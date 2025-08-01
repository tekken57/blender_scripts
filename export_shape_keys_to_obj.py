import bpy
import os
from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

class ExportShapeKeysOperator(bpy.types.Operator, ImportHelper):
    """Export all shape keys of the active object as individual OBJ files"""
    bl_idname = "wm.blender_export_shape_keys"
    bl_label = "Export Shape Keys as OBJs"
    filename_ext = ""
    use_filter_folder = True
    directory: StringProperty(name="Export Directory", subtype='DIR_PATH')

    def execute(self, context):
        obj = context.object

        if not obj or obj.type != 'MESH' or not obj.data.shape_keys:
            self.report({'ERROR'}, "No mesh object with shape keys selected.")
            return {'CANCELLED'}

        export_path = self.directory

        for sk in obj.data.shape_keys.key_blocks[1:]:
            sk.value = 0.0

        for sk in obj.data.shape_keys.key_blocks[1:]:
            sk.value = 1.0
            file_path = os.path.join(export_path, f"{sk.name}.obj")

            bpy.ops.export_scene.obj(
                filepath=file_path,
                use_selection=True,
                keep_vertex_order=True,
                use_uvs=False,
                use_normals=False
            )
            sk.value = 0.0

        self.report({'INFO'}, f"Shape keys exported to: {export_path}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ExportShapeKeysOperator)

def unregister():
    bpy.utils.unregister_class(ExportShapeKeysOperator)

if __name__ == "__main__":
    register()
