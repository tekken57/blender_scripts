import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
import os
import re

class ExportMaskListOperator(Operator, ExportHelper):
    """Export Mask List to a Text File"""
    bl_idname = "export_mask.list"
    bl_label = "Export Mask List"
    filename_ext = ".txt"
    
    filter_glob: bpy.props.StringProperty(
        default="*.txt",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        save_mask_list(self.filepath)
        return {'FINISHED'}

def convert_name_to_object_format(name):
    """
    Converts a Blender object name like '4 yCS_skin' to 'Object4'
    """
    # Extract the leading number using a regular expression
    match = re.match(r"(\d+)", name)
    if match:
        return f"Object{match.group(1)}"
    else:
        return name

def save_mask_list(filepath):
    """
    Exports the face indices of the selected objects to a text file.
    
    Args:
        filepath (str): Path to save the mask list.
    """
    # Ensure we are in Object Mode
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    
    # Open the file for writing
    with open(filepath, 'w') as out_file:
        # Loop through all selected objects
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                print(f"Processing object: {obj.name}")
                
                # Set active and go into Edit Mode if not already
                bpy.context.view_layer.objects.active = obj
                if bpy.context.object.mode != 'EDIT':
                    bpy.ops.object.mode_set(mode='EDIT')
                
                # Update view and get face selection
                bpy.ops.object.mode_set(mode='OBJECT')
                selected_faces = [f.index + 1 for f in obj.data.polygons if f.select]  # +1 to match 3ds Max

                if selected_faces:
                    # Convert the name to "ObjectX"
                    object_name = convert_name_to_object_format(obj.name)
                    
                    # Write the object name
                    out_file.write(f"{object_name}\n")
                    
                    # Join the face indices into a comma-separated string
                    face_list = ",".join(map(str, selected_faces))
                    out_file.write(f"{face_list}\n")
                    
                    print(f"Exported mask list for {object_name}: {face_list}")
                
                # Go back to Object Mode
                if bpy.context.object.mode != 'OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')

    print(f"Mask list exported successfully to {filepath}.")


# Register Operator
def register():
    bpy.utils.register_class(ExportMaskListOperator)


def unregister():
    bpy.utils.unregister_class(ExportMaskListOperator)


if __name__ == "__main__":
    register()
