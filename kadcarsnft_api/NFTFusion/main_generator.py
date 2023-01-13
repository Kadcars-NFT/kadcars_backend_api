import os
import bpy
from kadcar_factory import replace_object
from NFT_render_provider import *
from scene_utils import deselect_all_scene_objects
from scene_utils import delete_all_objects, import_scene_into_collection, set_scene_camera, export_scene_as_gltf
from render_utils import set_render_output_settings, configure_render_settings
from generators import *
import pandas as pd

delete_all_objects()

dirname = os.path.dirname(__file__)
path_to_assets_folder = os.path.join(dirname, 'assets')
path_to_background_config = os.path.join(dirname, 'background_config_files')

#read csv file containing metadata
# metadata_df = pd.read_csv(os.path.join(dirname, 'generator_scripts/output/edition 30/metadata.csv'))
metadata_df = pd.read_csv('K:/kadcars_metadata_batches/batch_0.csv')

kadcar_glbs = generate_kadcars_with_given_specs_gltfs(metadata_df, path_to_assets_folder)

#feed base cars glbs + rim glbs, return base cars * rims glbs
# kadcars_with_rims_gltf_file_names = generate_kadcars_with_rims_gltfs(base_car_glbs, rims_glbs, path_to_assets_folder)

#take x glbs, colorize, return x * color glbs
# kadcars_with_shading_gltf_file_names = generate_kadcars_with_shading_gltfs(kadcars_with_rims_gltf_file_names, path_to_assets_folder)

#place each car in each bg and return glbs
# kadcars_with_backgrounds_gltf_file_names = generate_scenes_w_kadcar_and_background_gltfs(kadcars_with_shading_gltf_file_names, path_to_assets_folder)