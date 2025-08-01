import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator

class RenameBonesFromTextOperator(Operator, ImportHelper):
    bl_idname = "object.rename_bones_from_text_fallback"
    bl_label = "Rename Bones from Text (Fallback)"
    bl_description = "Rename selected armature bones from a text file with fallback options"

    root_fallback_bone: StringProperty(
        name="Root Fallback Bone",
        description="Bone name to use if no mapping is found",
        default="J_Hips",
    )

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object.")
            return {'CANCELLED'}

        try:
            with open(self.filepath, 'r') as f:
                lines = f.read().splitlines()
                if len(lines) % 2 != 0:
                    self.report({'ERROR'}, "File format error. Use pairs of old/new names.")
                    return {'CANCELLED'}

                mapping = {lines[i].strip(): lines[i + 1].strip() for i in range(0, len(lines), 2)}

                for bone in obj.data.bones:
                    if bone.name in mapping:
                        bone.name = mapping[bone.name]
                    else:
                        parent = bone.parent
                        while parent:
                            if parent.name in mapping:
                                bone.name = mapping[parent.name]
                                break
                            parent = parent.parent
                        else:
                            fallback_name = next((old for old, new in mapping.items() if new == self.root_fallback_bone), None)
                            if fallback_name:
                                bone.name = fallback_name
                            else:
                                self.report({'WARNING'}, f"No mapping for bone '{bone.name}'.")

            self.report({'INFO'}, "Bones renamed successfully.")
            return {'FINISHED'}

        except FileNotFoundError:
            self.report({'ERROR'}, "File not found.")
            return {'CANCELLED'}

def register():
    bpy.utils.register_class(RenameBonesFromTextOperator)

def unregister():
    bpy.utils.unregister_class(RenameBonesFromTextOperator)

if __name__ == "__main__":
    register()
