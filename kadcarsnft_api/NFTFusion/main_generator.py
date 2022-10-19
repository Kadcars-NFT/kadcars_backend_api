import os
import bpy
from kadcar_factory import generate_kadcar_gltfs, replace_object
from NFT_render_provider import *
from scene_utils import deselect_all_scene_objects
from scene_utils import delete_all_objects, import_scene_into_collection, set_scene_camera, export_scene_as_gltf
from render_utils import set_render_output_settings, configure_render_settings
from generators import generate_kadcars_with_rims_gltfs, generate_kadcars_with_shading_gltfs, generate_scenes_w_kadcar_and_background_gltfs

delete_all_objects()

dirname = os.path.dirname(__file__)
path_to_assets_folder = os.path.join(dirname, 'assets')
path_to_background_config = os.path.join(dirname, 'background_config_files')

#take x base car glbs
base_car_glbs = [
    "00.glb"
]

rims_glbs = [
    # "rim_skinny.glb"
]

#feed base cars glbs + rim glbs, return base cars * rims glbs
kadcars_with_rims_gltf_file_names = generate_kadcars_with_rims_gltfs(base_car_glbs, rims_glbs, path_to_assets_folder)

#take x glbs, colorize, return x * color glbs
kadcars_with_shading_gltf_file_names = generate_kadcars_with_shading_gltfs(kadcars_with_rims_gltf_file_names, path_to_assets_folder)

#place each car in each bg and return glbs
kadcars_with_backgrounds_gltf_file_names = generate_scenes_w_kadcar_and_background_gltfs(kadcars_with_shading_gltf_file_names, path_to_assets_folder)