from select import select
import bpy
from bpy import context
import os
import math
import json
from scene_utils import *
from render_utils import *
from kadcar_factory import *

dirname = os.path.dirname(__file__)
path_to_glb_folder = os.path.join(dirname, 'assets')
path_to_jpeg_folder = os.path.join(dirname, 'assets')

delete_all_objects()

glb_dirList = os.listdir(path_to_glb_folder)
removeList = [".gitignore", ".DS_Store"] # If you have . files in your directory
glb_dirList = [x for x in glb_dirList if (x not in removeList)]

bpy.ops.import_scene.gltf(filepath=os.path.join(path_to_glb_folder, "garbage_w_lights.glb")) # Import .glb file to scene
#Import scene


set_car_location_in_scene(os.path.join(path_to_glb_folder, "blue_aligned.glb"), {'x':-0.000002, 'y':-2.35231, 'z':0}, {'w': 0.736, 'x':0.0, 'y':0.0, 'z':0.677})
move_collection_to_location('car', {'x':-0.000002, 'y':-2.35231, 'z':0.899999999}, {'w': 0.736, 'x':0.0, 'y':0.0, 'z':0.677})

obj_camera = bpy.data.objects["Camera"]
bpy.context.scene.camera = obj_camera

#Output scene settings
# outputRenderSettings()

#Render settings
configure_render_settings('CYCLES', 'CUDA', 'GPU', 200, 50)

#Customize the kadcar and scene
apply_hdri(os.path.join(path_to_glb_folder, 'bg.hdr'))
# colorize_kadcar_and_render("body", "primary", "Material.069")

rim_file = os.path.join(path_to_glb_folder, "rims_poc.glb")
# add_rims_to_kadcar(1, rim_file, 'lol')

#Set final render settings
set_render_output_settings(path_to_glb_folder, 'WEBP', True)


delete_all_objects()