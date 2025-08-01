import bpy
import bmesh

class Tekken57RigMeshesOperator(bpy.types.Operator):
    bl_idname = "object.tekken57_rig_meshes"
    bl_label = "Rig Meshes to 2k22 Skeleton"
    bl_description = "Transfer weights, rename meshes, and remap UVs to match 2k22 skeleton"

    rename_meshes: bpy.props.BoolProperty(
        name="Rename Meshes",
        description="Remove 'M_' prefix from mesh names",
        default=True
    )

    remap_uv: bpy.props.BoolProperty(
        name="Remap UVs",
        description="Increment UVs by 1 on the Y-axis",
        default=True
    )

    def execute(self, context):
        if len(context.selected_objects) < 2:
            self.report({'ERROR'}, "Select at least one target mesh and one source mesh (last selected).")
            return {'CANCELLED'}

        source_mesh = context.active_object
        target_meshes = [obj for obj in context.selected_objects if obj != source_mesh]
        parent_mesh = source_mesh.parent

        if not parent_mesh or parent_mesh.type != 'ARMATURE':
            self.report({'ERROR'}, "Source mesh must have an Armature parent.")
            return {'CANCELLED'}

        for target in target_meshes:
            bpy.ops.object.select_all(action='DESELECT')
            target.select_set(True)
            source_mesh.select_set(True)
            context.view_layer.objects.active = target

            bpy.ops.paint.weight_paint_toggle()
            bpy.ops.object.data_transfer(
                use_reverse_transfer=True,
                data_type='VGROUP_WEIGHTS',
                use_create=True,
                vert_mapping='POLYINTERP_NEAREST',
                layers_select_src='NAME',
                layers_select_dst='ALL',
                mix_mode='REPLACE'
            )

            modifier = target.modifiers.new(name="Armature", type='ARMATURE')
            modifier.object = parent_mesh

            bpy.ops.paint.weight_paint_toggle()

            if self.rename_meshes:
                if target.type == 'MESH' and target.name.lower().startswith("m_"):
                    target.name = target.name[2:]

            target.parent = parent_mesh
            target.matrix_parent_inverse = parent_mesh.matrix_world.inverted()

            if self.remap_uv and target.type == 'MESH':
                bpy.context.view_layer.objects.active = target
                bpy.ops.object.mode_set(mode='EDIT')
                bm = bmesh.from_edit_mesh(target.data)
                uv_layer = bm.loops.layers.uv.verify()
                for face in bm.faces:
                    for loop in face.loops:
                        loop[uv_layer].uv.y += 1.0
                bmesh.update_edit_mesh(target.data)
                bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Rigging and adjustments completed successfully.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(Tekken57RigMeshesOperator)

def unregister():
    bpy.utils.unregister_class(Tekken57RigMeshesOperator)

if __name__ == "__main__":
    register()
