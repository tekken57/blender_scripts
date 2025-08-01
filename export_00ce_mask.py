import bpy
import os
import struct
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty

class Export00CEMaskOperator(Operator, ExportHelper):
    """Export selected face masks to 00CE.pac binary format"""
    bl_idname = "export_00ce.mask"
    bl_label = "Export 00CE Mask File"
    filename_ext = ".pac"

    filter_glob: StringProperty(
        default="*.pac",
        options={'HIDDEN'},
    )

    def execute(self, context):
        return self.export_00ce_mask_file(context)

    def export_00ce_mask_file(self, context):
        object_data = []
        save_dir = os.path.dirname(self.filepath)

        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            obj_name = obj.name  # e.g., Object0
            try:
                index = int(obj_name.replace("Object", ""))
            except ValueError:
                self.report({'WARNING'}, f"Could not parse index from object name: {obj_name}")
                continue

            container_name = "M_Head" if index == 0 else "M_Body"
            original_obj_path = os.path.join(save_dir, f"{obj_name}.obj")
            if not os.path.isfile(original_obj_path):
                self.report({'WARNING'}, f"Original OBJ not found for {obj_name}. Expected at: {original_obj_path}")
                continue

            # Parse face list from OBJ file
            with open(original_obj_path, 'r') as f:
                original_faces = []
                for line in f:
                    if line.startswith("f "):
                        parts = line.strip().split()[1:]
                        verts = [int(p.split('/')[0]) for p in parts]
                        if len(verts) == 3:
                            original_faces.append(tuple(sorted(verts)))

            # Get selected faces from Blender object
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type="FACE")
            bpy.ops.object.mode_set(mode='OBJECT')

            selected_faces = []
            for face in obj.data.polygons:
                if face.select:
                    verts = [obj.data.loops[i].vertex_index + 1 for i in range(face.loop_start, face.loop_start + face.loop_total)]
                    try:
                        idx = original_faces.index(tuple(sorted(verts)))
                        selected_faces.append(idx)
                    except ValueError:
                        print(f"Face {verts} not found in {obj_name}")

            if not selected_faces:
                continue

            selected_faces.sort()
            ranges = []
            start = selected_faces[0]
            end = start
            for val in selected_faces[1:]:
                if val == end + 1:
                    end = val
                else:
                    ranges.append((start + 1, end + 1))  # convert to 1-based
                    start = val
                    end = val
            ranges.append((start + 1, end + 1))

            object_data.append((container_name, ranges))

        # Start writing binary PAC data
        binary = bytearray()
        binary += struct.pack('<I', 0)         # Unknown
        binary += struct.pack('<I', 0x0C)      # Offset to first block header
        binary += struct.pack('<I', len(object_data))  # Block count

        for container_name, ranges in object_data:
            masks = bytearray()
            for i, (start, end) in enumerate(ranges):
                masks += struct.pack('<I', 0x10)  # Block Header
                masks += struct.pack('<I', 0x28)  # Block Length (fixed)
                masks += struct.pack('<I', i)     # Index
                masks += struct.pack('<I', 1)     # Unknown
                masks += struct.pack('<I', 0x10)  # Offset
                masks += struct.pack('<I', 0x18)  # Offset
                masks += struct.pack('<I', 1)     # Count
                masks += struct.pack('<I', start)
                masks += struct.pack('<I', end)

            block = bytearray()
            block_size = 0x4C + len(masks) + 4
            block += struct.pack('<I', 0x4C)
            block += struct.pack('<I', block_size)
            name_padded = container_name.ljust(64, '\x00')
            block += name_padded.encode('ascii')[:64]
            block += struct.pack('<I', 0)
            block += struct.pack('<I', 1)
            block += masks

            binary += block

        with open(self.filepath, 'wb') as f:
            f.write(binary)

        self.report({'INFO'}, f"00CE Mask exported to {self.filepath}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(Export00CEMaskOperator)

def unregister():
    bpy.utils.unregister_class(Export00CEMaskOperator)
