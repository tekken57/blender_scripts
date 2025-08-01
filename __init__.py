import bpy

bl_info = {
    "name": "TKN57 Utilities",
    "author": "Tekken57",
    "version": (1, 0, 1),
    "blender": (3, 0, 0),
    "location": "Edit > TKN57 Utilities",
    "description": "Collection of Tekken57 workflow tools",
    "category": "Object",
}

# Menu class
class TKN57UtilitiesMenu(bpy.types.Menu):
    bl_label = "TKN57 Utilities"
    bl_idname = "TKN57_MT_utilities"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.blender_export_shape_keys", text="Export Shape Keys as OBJs")
        layout.operator("export.selected_bone_transforms_txt")
        layout.operator("export_weights.default", text="Export Bone Weights")
        layout.operator("export_weights.john_cena", text="Export Bone Weights (John Cena Base")
        layout.operator("export_weights.steve_austin", text="Export Bone Weights (Steve Austin Base")
        layout.operator("export_weights.charlotte_flair", text="Export Bone Weights (Charlotte Flair Base")
        layout.operator("export_weights_all.folder", text="Export Bone Weights (All Bones)")
        layout.operator("export.wavefront_normals_dialog")
        layout.operator("object.remove_modifiers_weights")
        layout.operator("object.rename_bones_from_text_fallback")
        layout.operator("object.tekken57_rig_meshes")
        layout.operator("import_scene.obj_preserve_order", text="Import OBJ (Preserve Order)")
        layout.operator("export_mask.list", text="Export Mask List")
        #layout.operator("export_00ce.mask", text="Export 00CE Mask File")  # ✅ NEW


def menu_func(self, context):
    self.layout.menu("TKN57_MT_utilities")

# Dialog wrapper for Wavefront Normals
class ExportWavefrontNormalsDialog(bpy.types.Operator):
    bl_idname = "export.wavefront_normals_dialog"
    bl_label = "Export Wavefront Normals"
    rotate_model: bpy.props.BoolProperty(name="Rotate Model", default=True)

    def execute(self, context):
        bpy.ops.export.wavefront_normals('INVOKE_DEFAULT', rotate_model=int(self.rotate_model))
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Remove Modifiers & Weights
class RemoveModifiersWeightsOperator(bpy.types.Operator):
    bl_idname = "object.remove_modifiers_weights"
    bl_label = "Remove Modifiers & Weights"

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                obj.modifiers.clear()
                obj.vertex_groups.clear()
        self.report({'INFO'}, "Modifiers and vertex groups cleared.")
        return {'FINISHED'}

# Classes in this file
classes = (
    TKN57UtilitiesMenu,
    ExportWavefrontNormalsDialog,
    RemoveModifiersWeightsOperator,
)

def register():
    # Import and register modules
    from . import blender_export_shape_keys
    from . import export_shape_keys_to_obj
    from . import export_bone_data
    from . import export_bone_weights_tkn57
    from . import export_bone_weights_john_cena
    from . import export_bone_weights_steve_austin
    from . import export_bone_weights_charlotte_flair
    from . import export_bone_weights_tkn57_all_bones
    from . import export_wavefront_batch_2k22_tkn57
    from . import remove_modifiers_and_weights_tkn57
    from . import rename_bones
    from . import tekken57_rig_meshes_2k22
    from . import export_masking_for_all_objects
    from . import import_obj_preserve_order
    #from . import export_00ce_mask  # ✅ NEW

    blender_export_shape_keys.register()
    export_shape_keys_to_obj.register()
    export_bone_data.register()
    export_bone_weights_tkn57.register()
    export_bone_weights_john_cena.register()
    export_bone_weights_steve_austin.register()
    export_bone_weights_charlotte_flair.register()
    export_bone_weights_tkn57_all_bones.register()
    export_wavefront_batch_2k22_tkn57.register()
    remove_modifiers_and_weights_tkn57.register()
    rename_bones.register()
    tekken57_rig_meshes_2k22.register()
    export_masking_for_all_objects.register()
    import_obj_preserve_order.register()
    #export_00ce_mask.register()  # ✅ NEW

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_edit.append(menu_func)

def unregister():
    bpy.types.TOPBAR_MT_edit.remove(menu_func)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    from . import blender_export_shape_keys
    from . import export_shape_keys_to_obj
    from . import export_bone_data
    from . import export_bone_weights_tkn57
    from . import export_bone_weights_john_cena
    from . import export_bone_weights_steve_austin
    from . import export_bone_weights_charlotte_flair
    from . import export_bone_weights_tkn57_all_bones
    from . import export_wavefront_batch_2k22_tkn57
    from . import remove_modifiers_and_weights_tkn57
    from . import rename_bones
    from . import tekken57_rig_meshes_2k22
    from . import export_masking_for_all_objects
    from . import import_obj_preserve_order
    #from . import export_00ce_mask  # ✅ NEW

    blender_export_shape_keys.unregister()
    export_shape_keys_to_obj.unregister()
    export_bone_data.unregister()
    export_bone_weights_tkn57.unregister()
    export_bone_weights_john_cena.unregister()
    export_bone_weights_steve_austin.unregister()
    export_bone_weights_charlotte_flair.unregister()
    export_bone_weights_tkn57_all_bones.unregister()
    export_wavefront_batch_2k22_tkn57.unregister()
    remove_modifiers_and_weights_tkn57.unregister()
    rename_bones.unregister()
    tekken57_rig_meshes_2k22.unregister()
    export_masking_for_all_objects.unregister()
    import_obj_preserve_order.unregister()
    #export_00ce_mask.unregister()  # ✅ NEW

if __name__ == "__main__":
    register()
