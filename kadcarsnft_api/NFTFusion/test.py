import bpy
from bpy import context
import os
import math
import json
from scene_utils import *
from render_utils import *
from render_settings import *

dirname = os.path.dirname(__file__)
path_to_glb_folder = os.path.join(dirname, 'assets') # If you are using Windows use r"\Users\Path\To\Folder"
path_to_jpeg_folder = os.path.join(dirname, 'assets')

delete_all_objects()

glb_dirList = os.listdir(path_to_glb_folder)

removeList = [".gitignore", ".DS_Store"] # If you have . files in your directory
glb_dirList = [x for x in glb_dirList if (x not in removeList)]

#import scene
bpy.ops.import_scene.gltf(filepath=os.path.join(path_to_glb_folder, "REDOSNOW.glb")) # Import .glb file to scene

#output scene settings
# outputRenderSettings()

#camera settings
obj_camera = bpy.data.objects["Camera"]
bpy.context.scene.camera = obj_camera

#render settings
set_render_device()
bpy.context.scene.render.engine = 'CYCLES'
bpy.data.scenes["Scene"].cycles.samples = 120#500

f = open('lights.json')
data = json.load(f)

curr = 0
cunt = 10

# for i in range(cunt):
#     md = data['lights'][0]
#     md["location"][0] = curr + i
#     create_area_light_object(md)

f.close()

#Colorize the kadcar and add HDRI
# colorize_kadcar_and_render("body", "primary", "Material.069")
apply_hdri(os.path.join(path_to_glb_folder, 'snowy_field_4k.hdr'))

set_render_output_settings(path_to_jpeg_folder, "JPEG")
bpy.ops.render.render(write_still=True) # Tell Blender to render an image


delete_all_objects()