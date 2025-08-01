import bpy

class RemoveModifiersWeightsOperator(bpy.types.Operator):
    bl_idname = "object.remove_modifiers_weights"
    bl_label = "Remove Modifiers and Weights"
    bl_description = "Removes all modifiers and vertex groups from selected mesh objects"

    def execute(self, context):
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']

        if not selected_meshes:
            self.report({'WARNING'}, "No mesh objects selected.")
            return {'CANCELLED'}

        for obj in selected_meshes:
            obj.modifiers.clear()
            obj.vertex_groups.clear()

        self.report({'INFO'}, "Modifiers and vertex groups cleared from selected meshes.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(RemoveModifiersWeightsOperator)

def unregister():
    bpy.utils.unregister_class(RemoveModifiersWeightsOperator)

if __name__ == "__main__":
    register()
