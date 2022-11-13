import os
import bpy
from scene_utils import *
from render_utils import configure_render_settings, set_render_output_settings
from io_utils import *

#TODO: fix output input paths
def generate_kadcar_nft_with_mountain_bg_old(path_to_asset_folder, kc_glb_paths, generate_render=False):
    configure_render_settings('CYCLES', 'CUDA', 'GPU', 200, 50)

    for glb in kc_glb_paths:
        import_background_into_scene(os.path.join(path_to_asset_folder, "backgrounds/mtn_no_car.glb"), 'background', os.path.join(path_to_asset_folder, "hdr_files/bg.hdr"))
        
        #move car to correct location in bg
        set_car_location_in_scene(os.path.join(path_to_asset_folder, glb), {'x': 0, 'y': 0, 'z':0.080608}, {'w': 1.0, 'x':0.0, 'y':0.0, 'z':0.0})

        #import scene (background)
        set_render_output_settings(path_to_asset_folder, 'WEBP', True)
        
        # delete_objects_from_collection_name('car')
        bpy.ops.wm.read_factory_settings(use_empty=True)


#TODO: add car location variables
def generate_kadcar_nft_with_background_gltf(path_to_asset_folder, kc_glb_name, bg_glb_name, hdr_file_name, background_name):
    dirname = os.path.dirname(__file__)
    kc_glb_path = os.path.join(path_to_asset_folder, 'with_shading/' + kc_glb_name)
    bg_glb_path = os.path.join(path_to_asset_folder, "backgrounds/" + bg_glb_name)
    hdr_file_path = os.path.join(path_to_asset_folder, "hdr_files/" + hdr_file_name)
    bg_config_path = os.path.join(dirname, 'background_config_files')

    bg_config = extract_data_from_json(os.path.join(bg_config_path, "backgrounds_config.json"))
    bg_config_data = bg_config[background_name]

    import_background_into_scene(bg_glb_path, 'background', hdr_file_path)
    
    set_car_location_in_scene(kc_glb_path, bg_config_data["location"], bg_config_data["quaternion_rotation"])

def generate_gltf_with_kadcar_in_background(filepath_prefix, kadcar_specs, kc_gltf_name):
    kc_glb_path = os.path.join(filepath_prefix, "completed_kadcars/" + kadcar_specs['Kadcar'] + "/" + kc_gltf_name)
    bg_glb_path = os.path.join(filepath_prefix, "backgrounds/" + kadcar_specs['Background'] + "_no_car.glb")
    hdr_file_path = os.path.join(filepath_prefix, "hdr_files/" + kadcar_specs['Background'] + "_background.hdr")
    bg_config_path = os.path.join(filepath_prefix, 'background_config_files')

    bg_config_data = extract_json_attribute_data(os.path.join(bg_config_path, "backgrounds_config.json"), kadcar_specs['Background'])

    # import_background_into_scene(bg_glb_path, 'background', hdr_file_path)
    import_scene_into_collection(bg_glb_path, 'background')
    set_scene_camera(cam_name="Camera")
    if kadcar_specs['Background'] != 'cyber':
        apply_hdri(hdr_file_path)
    set_car_location_in_scene(kc_glb_path, bg_config_data["location"], bg_config_data["quaternion_rotation"])