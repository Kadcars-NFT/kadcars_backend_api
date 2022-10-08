import os
import bpy
from scene_utils import set_car_location_in_scene, import_background_into_scene, delete_objects_from_collection_name
from render_utils import configure_render_settings, set_render_output_settings

#TODO: fix output input paths
def generate_kadcar_ft_with_mountain_bg(output_path, kc_glb_paths):
    configure_render_settings('CYCLES', 'CUDA', 'GPU', 200, 50)

    for glb in kc_glb_paths:
        import_background_into_scene(os.path.join(output_path, "mtn_no_car.glb"), 'background', os.path.join(output_path, "bg.hdr"))
        #move car to correct location in bg
        set_car_location_in_scene(os.path.join(output_path, glb), {'x': 0, 'y': 0, 'z':0.080608}, {'w': 1.0, 'x':0.0, 'y':0.0, 'z':0.0})

        #import scene (background)
        set_render_output_settings(output_path, 'WEBP', True)
        
        # delete_objects_from_collection_name('car')
        bpy.ops.wm.read_factory_settings(use_empty=True)