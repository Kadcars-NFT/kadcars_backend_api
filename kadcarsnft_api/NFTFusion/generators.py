from numpy import extract
import bpy
import os
from kadcar_factory import *
from scene_utils import *
from io_utils import *
from NFT_render_provider import *
from nft_metadata_handler import build_car_metadata
import pandas as pd

def generate_kadcars_with_given_specs_gltfs(kadcars_metadata_df, filepath_prefix):
    delete_all_objects_in_scene()

    k2_specs = kadcars_metadata_df[kadcars_metadata_df['Kadcar'] == 'k2']
    k2p_specs = kadcars_metadata_df[kadcars_metadata_df['Kadcar'] == 'k2p']
    
    #Set headers
    k2_specs.columns = kadcars_metadata_df.columns
    k2p_specs.columns = kadcars_metadata_df.columns

    # build_kadcars_using_metadata(k2_specs, filepath_prefix)
    # delete_all_objects_in_scene()
    build_kadcars_using_metadata(k2p_specs, filepath_prefix)
    build_kadcars_using_metadata(k2_specs, filepath_prefix)

def build_kadcars_using_metadata(kc_spec_list, filepath_prefix):
    delete_all_objects()
    f = None
    count = 0
    for index, kadcar_specs in kc_spec_list.iterrows():
        bg_config_path = os.path.join(filepath_prefix, 'background_config_files')
        bg_config_data = extract_json_attribute_data(os.path.join(bg_config_path, "backgrounds_config.json"), kadcar_specs['Background'])
        
        rim_gltf_full_path = os.path.join(filepath_prefix, "rims/" + kadcar_specs['Rim'] + '.glb')
        kc_gltf_full_path = os.path.join(filepath_prefix, "kadcars/" + kadcar_specs['Kadcar'] + '.glb')
        spoiler_gltf_full_path = os.path.join(filepath_prefix, "spoilers/" + kadcar_specs['Spoiler'] + '.glb')
        
        nft_name, kadcar_metadata = build_car_metadata(kadcar_specs)
        kadcar_export_file_name = nft_name + "_car.glb"
        nft_export_file_name = nft_name + "_nft.glb"
        nft_render_file_name = nft_name + "_render"

        #Import kadcar and add parts
        import_scene_into_collection(kc_gltf_full_path, 'kadcar')
        add_rims_to_kadcar(rim_gltf_full_path)

        if kadcar_specs['Kadcar'] == "k2":
            add_spoiler_to_kadcar(kadcar_specs, spoiler_gltf_full_path)
        else:
            clearance_light_gltf_full_path = os.path.join(filepath_prefix, "clearance_light/" + kadcar_specs['Spoiler'] + '.glb')
            add_clearance_light_to_pickup(kadcar_specs, clearance_light_gltf_full_path)
        
        #Add color and materials to car parts
        kadcar_metadata = add_materials_and_colorize_kadcar(filepath_prefix, kadcar_specs, kadcar_metadata)

        #Export car model
        select_only_objects_in_collection_name("kadcar")
        # export_scene_as_gltf(os.path.join(filepath_prefix, "completed_kadcars/" + kadcar_specs['Kadcar'] + "/" + kadcar_export_file_name), export_all=False)
        export_scene_as_gltf("K:/completed_kadcars/" + kadcar_specs['Kadcar'] + "/" + kadcar_export_file_name, export_all=False)
        delete_all_objects_in_scene()

        #Generate final gltf and export full nft model with metadata
        generate_gltf_with_kadcar_in_background(filepath_prefix, kadcar_specs, kadcar_export_file_name)
        # nft_output_path = os.path.join(filepath_prefix, "completed_nfts/" + kadcar_specs['Kadcar'] + "/" + kadcar_specs['Background'] + "/" + nft_name)
        nft_output_path = os.path.join("K:/", "completed_nfts/" + kadcar_specs['Kadcar'] + "/" + kadcar_specs['Background'] + "/" + nft_name)
        if not os.path.exists(nft_output_path):
            os.mkdir(nft_output_path)
        export_scene_as_gltf(os.path.join(nft_output_path + "/" + "nft"), True, 'GLB')
        add_metadata_to_gltf(os.path.join(nft_output_path + "/" + "nft.glb"), build_background_metadata(bg_config_data, kadcar_specs['Background']), ".glb")
        export_dictionary_to_json(kadcar_metadata, os.path.join(nft_output_path + "/" + nft_name))

        #Render and clear
        generate_render_for_nft(os.path.join(nft_output_path + "/" + nft_render_file_name), bg_config_data)
        delete_all_objects_in_scene()
        
        count += 1
        f = open('K:/batch_0.txt', 'a')
        f.write(str(count) + '  ' + nft_name + '\n')
        f.close()

def generate_render_for_nft(destination_file, bg_config_data):
    configure_render_settings('CYCLES', 'CUDA', 'GPU', 200, 50)
    set_render_output_settings(destination_file, 'WEBP', bg_config_data['render_settings']['res_x'], bg_config_data['render_settings']['res_y'], True)