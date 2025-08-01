import bpy
import os
from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from bpy_extras.io_utils import ExportHelper

# Bone name to ID map from 3ds Max
bone_name_to_max_id = {
    "J_Clavicle_L": 0, "J_Head": 1, "J_Neck": 2, "J_Chest": 3, "H_Neck_tw": 4,
    "J_Clavicle_R": 5, "J_Spine2": 6, "J_Shoulder_R": 7, "J_Spine1": 8, "J_Hips": 9,
    "J_Elbow_R": 10, "J_Shoulder_L": 11, "J_Elbow_L": 12, "H_Elbow_R_tw02": 13,
    "J_Wrist_R": 14, "H_Elbow_R_tw01": 15, "J_MiddleF1_R": 16, "J_ThumbF1_R": 17,
    "J_PinkyF1_R": 18, "J_ThumbF2_R": 19, "J_RingF1_R": 20, "J_IndexF1_R": 21,
    "J_PinkyF3_R": 22, "J_PinkyF2_R": 23, "J_RingF3_R": 24, "J_RingF2_R": 25,
    "J_MiddleF3_R": 26, "J_MiddleF2_R": 27, "J_IndexF3_R": 28, "J_IndexF2_R": 29,
    "J_ThumbF3_R": 30, "H_Ebw_In_R": 31, "H_Ebw_Out_R": 32, "H_Elbow_L_tw02": 33,
    "J_Wrist_L": 34, "H_Elbow_L_tw01": 35, "J_MiddleF1_L": 36, "J_ThumbF1_L": 37,
    "J_PinkyF1_L": 38, "J_ThumbF2_L": 39, "J_RingF1_L": 40, "J_IndexF1_L": 41,
    "J_PinkyF3_L": 42, "J_PinkyF2_L": 43, "J_RingF3_L": 44, "J_RingF2_L": 45,
    "J_MiddleF3_L": 46, "J_MiddleF2_L": 47, "J_IndexF3_L": 48, "J_IndexF2_L": 49,
    "J_ThumbF3_L": 50, "H_Ebw_In_L": 51, "H_Ebw_Out_L": 52, "J_Leg_R": 53,
    "J_Leg_L": 54, "J_Foot_R": 55, "J_Knee_R": 56, "J_Toe_R": 57, "J_Foot_L": 58,
    "J_Knee_L": 59, "J_Toe_L": 60, "J_Eye_R": 61, "J_Eye_L": 62, "J_Jaw": 63,
    "J_Tongue1": 64, "J_Tongue2": 65, "J_Tongue3": 66, "J_Tongue4": 67
}

class ExportBoneWeightsOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "export_weights.default"
    bl_label = "Export Bone Weights"
    filename_ext = ""
    use_filter_folder = True
    directory: StringProperty(name="Export Folder", subtype='DIR_PATH')

    def execute(self, context):
        export_dir = self.directory
        #export_dir = self.filepath
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        selected_meshes = [o for o in context.selected_objects if o.type == 'MESH']

        if not selected_meshes:
            self.report({'WARNING'}, "No mesh objects selected.")
            return {'CANCELLED'}

        for idx, obj in enumerate(selected_meshes):
            txt_path = os.path.join(export_dir, f"Object{idx}.txt")

            try:
                with open(txt_path, 'w') as out:
                    for v in obj.data.vertices:
                        weights = []
                        for g in v.groups:
                            vg = obj.vertex_groups[g.group]
                            bone_id = bone_name_to_max_id.get(vg.name)
                            if bone_id is not None:
                                weights.append(f"{bone_id} {g.weight:.6f}")
                        out.write(" ".join(weights) + "\n")
            except Exception as e:
                self.report({'ERROR'}, f"Failed to export {obj.name}: {e}")
                continue

        self.report({'INFO'}, f"Weights exported to: {export_dir}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ExportBoneWeightsOperator)

def unregister():
    bpy.utils.unregister_class(ExportBoneWeightsOperator)

if __name__ == "__main__":
    register()
