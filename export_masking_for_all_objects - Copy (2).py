import bpy
import bmesh
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
import os
import re

class ExportMaskListOperator(Operator, ExportHelper):
    """Export Mask List Matching Original OBJ Face Order"""
    bl_idname = "export_mask.list"
    bl_label = "Export Mask List"
    filename_ext = ".txt"

    filter_glob: bpy.props.StringProperty(
        default="*.txt",
        options={'HIDDEN'},
        maxlen=255,
    )

    # Change: use StringProperty instead of FILE_PATH to avoid dialog conflict
    obj_source_path: bpy.props.StringProperty(
        name="OBJ Source Path",
        description="Enter full path to the original imported OBJ file"
    )

    def execute(self, context):
        if not self.obj_source_path or not os.path.isfile(self.obj_source_path):
            self.report({'ERROR'}, "You must enter a valid path to the OBJ source file")
            return {'CANCELLED'}
        save_mask_list(self.filepath, self.obj_source_path)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "obj_source_path")

def convert_name_to_object_format(name):
    match = re.match(r"(\d+)", name)
    return f"Object{match.group(1)}" if match else name

def parse_obj_faces(filepath):
    faces = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("f "):
                parts = line.strip().split()[1:]
                verts = [int(p.split('/')[0]) for p in parts]
                if len(verts) == 3:
                    faces.append(tuple(sorted(verts)))
    return faces

def save_mask_list(output_path, obj_source_path):
    obj_faces = parse_obj_faces(obj_source_path)

    with open(output_path, 'w') as out_file:
        for obj in bpy.context.selected_objects:
            if obj.type != 'MESH':
                continue

            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')

            bm = bmesh.from_edit_mesh(obj.data)
            bm.faces.ensure_lookup_table()

            selected_indices = []
            for face in bm.faces:
                if face.select:
                    obj_indices = [loop.vert.index + 1 for loop in face.loops]
                    key = tuple(sorted(obj_indices))
                    try:
                        face_index = obj_faces.index(key) + 1
                        selected_indices.append(face_index)
                    except ValueError:
                        print(f"⚠️ Face {key} not found in OBJ source")

            bpy.ops.object.mode_set(mode='OBJECT')

            if selected_indices:
                object_name = convert_name_to_object_format(obj.name)
                out_file.write(f"{object_name}\n")
                face_list = ",".join(map(str, selected_indices))
                out_file.write(f"{face_list}\n")
                print(f"✅ Exported {len(selected_indices)} mapped faces for {object_name}")

    print(f"✅ Mask list written to: {output_path}")

def register():
    bpy.utils.register_class(ExportMaskListOperator)

def unregister():
    bpy.utils.unregister_class(ExportMaskListOperator)
