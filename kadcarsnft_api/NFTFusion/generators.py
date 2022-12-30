from numpy import extract
import bpy
import os
from kadcar_factory import *
from scene_utils import *
from io_utils import *
from NFT_render_provider import *
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
        # add_rims_to_kadcar(rim_gltf_full_path)

        if kadcar_specs['Kadcar'] == "k2":
            add_spoiler_to_kadcar(kadcar_specs, spoiler_gltf_full_path)
        else:
            clearance_light_file = "clearance_light_1"
            if kadcar_specs['Spoiler'] == 'spoiler_2':
                clearance_light_file = "clearance_light_2"
            kadcar_specs['Spoiler'] = clearance_light_file
            
            clearance_light_gltf_full_path = os.path.join(filepath_prefix, "clearance_light/" + clearance_light_file + '.glb')
            add_clearance_light_to_pickup(kadcar_specs, clearance_light_gltf_full_path)
        
        #Add color and materials to car parts
        kadcar_metadata = add_materials_and_colorize_kadcar(filepath_prefix, kadcar_specs, kadcar_metadata)

        #Export car model
        select_only_objects_in_collection_name("kadcar")
        export_scene_as_gltf(os.path.join(filepath_prefix, "completed_kadcars/" + kadcar_specs['Kadcar'] + "/" + kadcar_export_file_name), export_all=False)
        delete_all_objects_in_scene()

        #Generate final gltf and export full nft model with metadata
        generate_gltf_with_kadcar_in_background(filepath_prefix, kadcar_specs, kadcar_export_file_name)
        nft_output_path = os.path.join(filepath_prefix, "completed_nfts/" + kadcar_specs['Kadcar'] + "/" + kadcar_specs['Background'] + "/" + nft_name)
        if not os.path.exists(nft_output_path):
            os.mkdir(nft_output_path)
        # export_scene_as_gltf(os.path.join(nft_output_path + "/" + nft_export_file_name), True, 'GLTF_EMBEDDED')
        # add_metadata_to_gltf(os.path.join(nft_output_path + "/" + nft_export_file_name), build_background_metadata(bg_config_data), ".glb")
        export_dictionary_to_json(kadcar_metadata, os.path.join(nft_output_path + "/" + nft_name))

        #Render and clear
        generate_render_for_nft(os.path.join(nft_output_path + "/" + nft_render_file_name), bg_config_data)
        delete_all_objects_in_scene()


def generate_render_for_nft(destination_file, bg_config_data):
    configure_render_settings('CYCLES', 'CUDA', 'GPU', 200, 50)
    set_render_output_settings(destination_file, 'WEBP', bg_config_data['render_settings']['res_x'], bg_config_data['render_settings']['res_y'], True)

#####################################
############## OLD ##################
#####################################

def generate_kadcars_with_rims_gltfs(kadcar_gltf_file_names, rims_gltf_file_names, filepath_prefix):
    delete_all_objects_in_scene()
    result_gltf_filenames = kadcar_gltf_file_names.copy()

    i = 0
    j = 0
    for kc_gltf in kadcar_gltf_file_names:
        for rim_gltf in rims_gltf_file_names:
            export_file_name = kc_gltf + str(i) + str(j) + '.glb'
            kc_gltf_full_path = os.path.join(filepath_prefix, "kadcars/" + kc_gltf)
            rim_gltf_full_path = os.path.join(filepath_prefix, "rims/" + rim_gltf)

            add_rims_to_kadcar(kc_gltf_full_path, rim_gltf_full_path)
            export_scene_as_gltf(os.path.join('with_rims/', export_file_name))
            delete_all_objects_in_scene()
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
    bg_names = ['beach']
    result_gltf_filenames = []

    configure_render_settings('CYCLES', 'CUDA', 'GPU', 200, 50)
    
    for bg in bg_names:
        for kc_gltf in kadcars_with_rims_and_shading:
            generate_kadcar_nft_with_background_gltf(filepath_prefix, kc_gltf, bg + "_no_car.glb", bg + "_background.hdr", bg)

            # export_scene_as_gltf(os.path.join(filepath_prefix, 'with_backgrounds/' + kc_gltf.split('.')[0] + '_' + bg), export_all=True)

            #import scene (background)
            set_render_output_settings(os.path.join(filepath_prefix, 'final_nft_renders/' + kc_gltf.split('.')[0] + '_' + bg + '_render'), 'WEBP', 1920, 1080, True)
            
            # delete_objects_from_collection_name('car')
            delete_all_objects_in_scene()

    return result_gltf_filenames

def generate_renders_from_given_scenes(files_to_render, file_prefix, material_name, scene_name):
    configure_render_settings('CYCLES', 'CUDA', 'GPU', 200, 50)

    for file in files_to_render:
        filepath = os.path.join(file_prefix, "with_backgrounds/" + material_name + "/" + file)
        output_filepath = os.path.join(file_prefix, "final_nft_renders/" + material_name + "/" + file.split('/')[0])

        import_scene_into_collection(filepath, 'scene')
        set_scene_camera(cam_name="Camera_Orientation")
        add_lights_to_scene("lights.json", os.path.dirname(__file__))
        customize_world_shader_nodes(os.path.join(file_prefix, "hdr_files/" + scene_name + "_background.hdr"))
        set_render_output_settings(output_filepath, 'WEBP', 1920, 1080, True)
        delete_all_objects_in_scene()

def generate_kadcar_gltfs(materials_file, kadcar_file, format='glb'):
    delete_all_objects()
    material_collection = import_scene_into_collection(materials_file, 'materials')

    #Prep car
    car_collection = import_scene_into_collection(kadcar_file, 'car')
    
    f = open('car_parts.json')
    data = json.load(f)
    car_parts = data["body"]
    f.close()

    car_part_objects = get_objects_from_collection_by_names(car_collection, car_parts)

    glb_file_names = []

    for obj in material_collection.all_objects:
        if obj.type == 'MESH':
            file_name = 'kadcar_' + obj.name + '.' + format
            print("type: "+obj.type+"   material: "+obj.material_slots[0].name )
            transfer_materials_bulk(clean=True, src=obj, target_object_names=car_part_objects)
            select_only_objects_in_collection(car_collection)
            export_scene_as_gltf(file_name)
            glb_file_names.append(file_name)
            bpy.ops.wm.read_factory_settings(use_empty=True)

    delete_all_objects()
    return glb_file_names