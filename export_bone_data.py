import bpy
from bpy_extras.io_utils import ExportHelper
from mathutils import Euler
from math import radians

class ExportSelectedBoneTransformsOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "export.selected_bone_transforms_txt"
    bl_label = "Export Selected Bone Transforms"
    filename_ext = ".txt"

    def execute(self, context):
        armature = context.object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select an armature object in Pose Mode.")
            return {'CANCELLED'}

        selected_bones = context.selected_pose_bones
        if not selected_bones:
            self.report({'ERROR'}, "No bones selected in Pose Mode.")
            return {'CANCELLED'}

        correction_matrix = Euler((radians(90), 0, radians(-90)), 'XYZ').to_matrix().to_4x4()

        filepath = self.filepath
        if not filepath.lower().endswith('.txt'):
            filepath += '.txt'

        with open(filepath, 'w') as file:
            for bone in selected_bones:
                bone_name = bone.name
                local_matrix = bone.parent.matrix.inverted() @ bone.matrix if bone.parent else bone.matrix
                adjusted_matrix = correction_matrix @ local_matrix
                translation = adjusted_matrix.to_translation()

                file.write(f'"{bone_name}"\n')
                file.write(f'tx {translation.z:.6f}\n')
                file.write(f'ty {-translation.y:.6f}\n')
                file.write(f'tz {translation.x:.6f}\n\n')

        self.report({'INFO'}, f'Successfully exported bone transforms to {filepath}')
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ExportSelectedBoneTransformsOperator)

def unregister():
    bpy.utils.unregister_class(ExportSelectedBoneTransformsOperator)

if __name__ == "__main__":
    register()
