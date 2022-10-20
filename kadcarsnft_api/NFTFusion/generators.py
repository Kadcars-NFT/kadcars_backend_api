from numpy import extract
import bpy
import os
from kadcar_factory import add_rims_to_kadcar, add_materials_to_kadcar
from scene_utils import export_scene_as_gltf, delete_all_objects_in_scene
from io_utils import extract_data_from_json
from NFT_render_provider import *
from numba import jit

@jit
def generate_kadcars_with_rims_gltfs(kadcar_gltf_file_names, rims_gltf_file_names, filepath_prefix):
    delete_all_objects_in_scene()
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
            delete_all_objects_in_scene()
            result_gltf_filenames.append(export_file_name)
            j += 1
        i += 1
    return result_gltf_filenames

@jit
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

@jit
def generate_scenes_w_kadcar_and_background_gltfs(kadcars_with_rims_and_shading, filepath_prefix):
    bg_names = ['mountain']
    result_gltf_filenames = []

    configure_render_settings('CYCLES', 'CUDA', 'GPU', 200, 50)
    
    for bg in bg_names:
        for kc_gltf in kadcars_with_rims_and_shading:
            generate_kadcar_nft_with_background_gltf(filepath_prefix, kc_gltf, bg + "_no_car.glb", bg + "_background.hdr", bg)

            export_scene_as_gltf(os.path.join(filepath_prefix, 'with_backgrounds/' + kc_gltf.split('.')[0] + '_' + bg), export_all=True)

            #import scene (background)
            # set_render_output_settings(os.path.join(filepath_prefix, 'final_nft_renders/' + kc_gltf.split('.')[0] + '_' + bg + '_render'), 'WEBP', True)
            
            # delete_objects_from_collection_name('car')
            delete_all_objects_in_scene()

    return result_gltf_filenames