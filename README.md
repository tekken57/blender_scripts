# blender_scripts
A collection of my script for creating custom WWE 2k19 model using Blender and X-Rey 5.1. 

**Installation Instructions**
Download the release and copy the extracted TKN57_Utilities folder into your Blender addons folder e.g. C:\Program Files\Blender Foundation\Blender 3.1\3.1\scripts\addons\
Open Blender, click on Edit-Preferences and then click on the addons tab. Then search for TKN57. Select the checkbox to enable the plugin. You should have a new TKN57 Utilies menu item under the edit menu in Blender. 

**Usage instructions**
For a full tutorial on how to install and use the scripts, watch this tutorial on my YouTube Channel: https://www.youtube.com/watch?v=7U-_d36-oT8

**Rigging Issues**
If you experiece issues with random "spikes" on your models when rigging to the Cena, Austin or Charlotte models you need to set the bone limit on the rig to a maximum of 7. Do this by selecting the mesh and click on object-clean up-limit total vertex groups from the blender menu. Then set the value to 7 which is the number of weights you assigned when creating the yobj. Rexport and reimport the weights on those meshes. 
