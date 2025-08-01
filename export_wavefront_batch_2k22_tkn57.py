import bpy
import os
from bpy_extras.io_utils import ExportHelper

class ExportWavefrontNormalsOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "export.wavefront_normals"
    bl_label = "Export Wavefront Normals"
    filename_ext = ""
    use_filter_folder = True

    rotate_model: bpy.props.BoolProperty(
        name="Rotate Model (Y/Z inversion)",
        description="Invert Y/Z axis if enabled",
        default=True
    )

    def execute(self, context):
        selected_objects = context.selected_objects
        depsgraph = context.evaluated_depsgraph_get()

        if not selected_objects:
            self.report({'ERROR'}, "No objects selected.")
            return {'CANCELLED'}

        for idx, mesh_obj in enumerate(selected_objects):
            if mesh_obj.type != 'MESH':
                continue

            mesh_name = mesh_obj.name.replace(":skinned", "")
            file_full_path = os.path.join(self.filepath, f"{idx}_{mesh_name}_normals.obj")

            mesh_eval = mesh_obj.evaluated_get(depsgraph).to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
            mesh_eval.calc_normals_split()

            verts = mesh_eval.vertices
            loops = mesh_eval.loops
            polygons = mesh_eval.polygons
            uv_layer = mesh_eval.uv_layers.active.data

            with open(file_full_path, 'w') as file:
                file.write("# Wavefront OBJ exported from Blender\n")
                file.write(f"# Vertices: {len(verts)}\n")
                file.write(f"# UVs: {len(verts)}\n")
                file.write(f"# Normals: {len(verts)}\n")

                for v in verts:
                    if self.rotate_model:
                        file.write(f"v {v.co.x} {-v.co.y} {-v.co.z}\n")
                    else:
                        file.write(f"v {v.co.x} {v.co.y} {v.co.z}\n")

                vert_normals = [None] * len(verts)
                for loop in loops:
                    vert_normals[loop.vertex_index] = loop.normal

                for n in vert_normals:
                    if self.rotate_model:
                        file.write(f"vn {-n.x} {-n.y} {n.z}\n")
                    else:
                        file.write(f"vn {-n.x} {n.y} {-n.z}\n")

                vert_uvs = [None] * len(verts)
                for loop in loops:
                    vert_uvs[loop.vertex_index] = uv_layer[loop.index].uv

                for uv in vert_uvs:
                    file.write(f"vt {uv.x} {uv.y} 0\n")

                file.write(f"g {mesh_name}\n")
                file.write("s 1\n")

                for poly in polygons:
                    face_str = "f"
                    vertices = reversed(poly.vertices) if self.rotate_model else poly.vertices
                    for vert_idx in vertices:
                        idx1 = vert_idx + 1
                        face_str += f" {idx1}/{idx1}/{idx1}"
                    file.write(face_str + "\n")

            mesh_obj.to_mesh_clear()

        self.report({'INFO'}, f"Successfully exported to: {self.filepath}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ExportWavefrontNormalsOperator)

def unregister():
    bpy.utils.unregister_class(ExportWavefrontNormalsOperator)

if __name__ == "__main__":
    register()
