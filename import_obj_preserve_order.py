import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from pathlib import Path

class ImportObjPreserveOrderOperator(Operator, ImportHelper):
    """Import multiple OBJ files and preserve face order"""
    bl_idname = "import_scene.obj_preserve_order"
    bl_label = "Import OBJ (Preserve Face Order)"
    bl_options = {'UNDO'}

    filename_ext = ".obj"
    filter_glob: bpy.props.StringProperty(default="*.obj", options={'HIDDEN'})
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)

    def execute(self, context):
        directory = Path(self.filepath).parent
        imported = []

        for file_entry in self.files:
            obj_path = directory / file_entry.name

            # Import OBJ file using built-in minimal call
            bpy.ops.import_scene.obj(filepath=str(obj_path),split_mode='OFF')

            # Tag newly selected mesh objects with custom property
            for obj in context.selected_objects:
                if obj.type == 'MESH':
                    obj["original_obj_path"] = str(obj_path.resolve())
                    imported.append(obj.name)

        self.report({'INFO'}, f"✅ Imported: {', '.join(imported)}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ImportObjPreserveOrderOperator)

def unregister():
    bpy.utils.unregister_class(ImportObjPreserveOrderOperator)
