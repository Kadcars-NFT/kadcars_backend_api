import os
import bpy
from scene_utils import set_car_location_in_scene, import_background_into_scene, delete_objects_from_collection_name
from render_utils import configure_render_settings, set_render_output_settings

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
def generate_kadcar_nft_with_background_gltf(path_to_asset_folder, kc_glb_name, bg_glb_name, hdr_file_name):
    kc_glb_path = os.path.join(path_to_asset_folder, kc_glb_name)
    bg_glb_path = os.path.join(path_to_asset_folder, "backgrounds/" + bg_glb_name)
    hdr_file_path = os.path.join(path_to_asset_folder, "hdr_files/" + hdr_file_name)

    import_background_into_scene(bg_glb_path, 'background', hdr_file_path)
    
    set_car_location_in_scene(kc_glb_path, {'x': 0, 'y': 0, 'z':0.080608}, {'w': 1.0, 'x':0.0, 'y':0.0, 'z':0.0})