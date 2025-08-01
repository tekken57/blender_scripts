import bpy
import bmesh
import os
import re

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

def save_mask_list(output_path):
    output_dir = os.path.dirname(output_path)

    with open(output_path, 'w') as out_file:
        for obj in bpy.context.selected_objects:
            if obj.type != 'MESH':
                continue

            obj_path = os.path.join(output_dir, obj.name + ".obj")
            if not os.path.isfile(obj_path):
                print(f"❌ Skipping {obj.name}: '{obj.name}.obj' not found in export directory")
                continue

            obj_faces = parse_obj_faces(obj_path)

            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bm = bmesh.from_edit_mesh(obj.data)
            bm.faces.ensure_lookup_table()

            selected_indices = []
            for face in bm.faces:
                if face.select:
                    verts = [loop.vert.index + 1 for loop in face.loops]
                    key = tuple(sorted(verts))
                    try:
                        face_index = obj_faces.index(key) + 1
                        selected_indices.append(face_index)
                    except ValueError:
                        print(f"⚠️ Face {key} not found in {obj.name}")

            bpy.ops.object.mode_set(mode='OBJECT')

            if selected_indices:
                object_name = convert_name_to_object_format(obj.name)
                out_file.write(f"{object_name}\n")
                out_file.write(",".join(map(str, selected_indices)) + "\n")
                print(f"✅ Exported {len(selected_indices)} faces for {object_name}")

    print(f"✅ Finished exporting to: {output_path}")

# Blender operator
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator

class ExportMaskListOperator(Operator, ExportHelper):
    """Export Selected Face Indices to Mask List"""
    bl_idname = "export_mask.list"
    bl_label = "Export Mask List"
    filename_ext = ".txt"

    filter_glob: bpy.props.StringProperty(
        default="*.txt",
        options={'HIDDEN'},
    )

    def execute(self, context):
        save_mask_list(self.filepath)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ExportMaskListOperator)

def unregister():
    bpy.utils.unregister_class(ExportMaskListOperator)
