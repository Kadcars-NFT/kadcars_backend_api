from numpy import extract
import bpy
import os
from kadcar_factory import add_rims_to_kadcar, add_materials_to_kadcar
from scene_utils import export_scene_as_gltf, clear_scene_except_cameras, delete_all_objects_in_scene
from io_utils import extract_data_from_json
from NFT_render_provider import *

def generate_kadcars_with_rims_gltfs(kadcar_gltf_file_names, rims_gltf_file_names, filepath_prefix):
    clear_scene_except_cameras()
    result_gltf_filenames = kadcar_gltf_file_names.copy()

    i = 0
    j = 0
    for kc_gltf in kadcar_gltf_file_names:
        for rim_gltf in rims_gltf_file_names:
            export_file_name = str(i) + str(j) + '.glb'
            kc_gltf_full_path = os.path.join(filepath_prefix, kc_gltf)
            rim_gltf_full_path = os.path.join(filepath_prefix, rim_gltf)

            add_rims_to_kadcar(kc_gltf_full_path, rim_gltf_full_path)
            export_scene_as_gltf(os.path.join('with_rims/', export_file_name))
            clear_scene_except_cameras()
            result_gltf_filenames.append(export_file_name)
            j += 1
        i += 1
    return result_gltf_filenames

def generate_kadcars_with_shading_gltfs(kadcars_with_rims_gltf_file_names, filepath_prefix):
    delete_all_objects_in_scene()
    result_gltf_filenames = []

    dirname = os.path.dirname(__file__)
    colorize_json = os.path.join(dirname, 'colorize.json')
    car_parts_to_colorize = extract_data_from_json(colorize_json)['colorize']

    for kc_gltf in kadcars_with_rims_gltf_file_names:
        kc_gltf_filepath = os.path.join(filepath_prefix, "with_rims/" + kc_gltf)
        kc_gltf_with_shading_filenames = add_materials_to_kadcar(kc_gltf_filepath, car_parts_to_colorize, kc_gltf)
        result_gltf_filenames += kc_gltf_with_shading_filenames
        delete_all_objects_in_scene()
        
    return result_gltf_filenames

def generate_scenes_w_kadcar_and_background_gltfs(kadcars_with_rims_and_shading, filepath_prefix):
    bg_names = ['MOUNTAIN']
    result_gltf_filenames = []

    configure_render_settings('CYCLES', 'CUDA', 'GPU', 200, 50)
    
    for bg in bg_names:
        for kc_gltf in kadcars_with_rims_and_shading:
            print(kc_gltf)
            if bg == 'MOUNTAIN':
                generate_kadcar_nft_with_background_gltf(filepath_prefix, kc_gltf, "mountain_no_car.glb", "mtn_bg.hdr")
            elif bg == 'BEACH':
                generate_kadcar_nft_with_background_gltf(filepath_prefix, kc_gltf, "beach_no_car.glb", "mtn_bg.hdr")
            elif bg == 'SNOW':
                generate_kadcar_nft_with_background_gltf(filepath_prefix, kc_gltf, "snow_no_car.glb", "snow_bg.hdr")
            elif bg == 'STORAGE':
                generate_kadcar_nft_with_background_gltf(filepath_prefix, kc_gltf, "storage_no_car.glb", "mtn_bg.hdr")
            elif bg == 'CYBER':
                generate_kadcar_nft_with_background_gltf(filepath_prefix, kc_gltf, "cyber_no_car.glb", "mtn_bg.hdr")

             #import scene (background)
            set_render_output_settings(os.path.join(filepath_prefix, 'final_nft_renders/' + kc_gltf.split('.')[0] + '_render'), 'WEBP', True)
            
            # delete_objects_from_collection_name('car')
            clear_scene_except_cameras()

    return result_gltf_filenames