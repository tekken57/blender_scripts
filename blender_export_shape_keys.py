import bpy
from bpy_extras.io_utils import ExportHelper
import os

class ExportShapeKeysOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "wm.blender_export_shape_keys"
    bl_label = "Export Shape Keys as OBJs"
    filename_ext = ""
    use_filter_folder = True

    def execute(self, context):
        export_path = self.filepath
        obj = context.object

        if obj.type != 'MESH' or not obj.data.shape_keys:
            self.report({'ERROR'}, "Select a mesh object with shape keys.")
            return {'CANCELLED'}

        # Reset all shape keys to 0 (skipping Basis)
        for skblock in obj.data.shape_keys.key_blocks[1:]:
            skblock.value = 0

        # Iterate and export shape keys
        for skblock in obj.data.shape_keys.key_blocks[1:]:
            skblock.value = 1.0
            obj_name = skblock.name + ".obj"
            file_path = os.path.join(export_path, obj_name)
            bpy.ops.export_scene.obj(filepath=file_path, keep_vertex_order=True, use_uvs=False, use_normals=False, use_selection=True)
            skblock.value = 0

        self.report({'INFO'}, f"Shape keys exported successfully to: {export_path}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ExportShapeKeysOperator)

def unregister():
    bpy.utils.unregister_class(ExportShapeKeysOperator)

if __name__ == "__main__":
    register()
