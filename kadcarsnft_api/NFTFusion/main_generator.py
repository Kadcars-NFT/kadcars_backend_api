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

def generate_nfts(batch_number):
    #read csv file containing metadata
    # metadata_df = pd.read_csv(os.path.join(dirname, 'generator_scripts/output/edition 30/metadata.csv'))
    metadata_df = pd.read_csv('K:/kadcars_metadata_batches/batch_' + str(batch_number) + '.csv')

    kadcar_glbs = generate_kadcars_with_given_specs_gltfs(metadata_df, path_to_assets_folder, 'batch_' + str(batch_number))

print("How many batches are you generating?")
num_batches = input()

print("Type starting batch number")
starting_batch = input()

if num_batches < 1:
    exit() 

for i in range(num_batches):
    generate_nfts(starting_batch)
    starting_batch += 1