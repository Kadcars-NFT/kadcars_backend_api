import os
import bpy
from kadcar_factory import generate_kadcar_gltfs, replace_object
from NFT_render_provider import *
from scene_utils import deselect_all_scene_objects
from scene_utils import delete_all_objects, import_scene_into_collection, set_scene_camera, export_scene_as_gltf
from render_utils import set_render_output_settings, configure_render_settings

delete_all_objects()

scene_names = ['BEACH', 'MOUNTAIN', 'SNOW']

dirname = os.path.dirname(__file__)
path_to_glb_folder = os.path.join(dirname, 'assets')
path_to_jpeg_folder = os.path.join(dirname, 'assets')

materials_file = os.path.join(path_to_glb_folder, 'material_cubes.glb')
kadcar_file = os.path.join(path_to_glb_folder, 'aligned_renamed_rims.glb')

#create kadcar glbs with customization
# kc_glb_list = generate_kadcar_gltfs(materials_file, kadcar_file, 'glb')
kc_glb_list = [
    'kadcar_Material.001.glb',
    # 'kadcar_Material.002.glb',
    # 'kadcar_Material.003.glb',
    # 'kadcar_Material.005.glb',
    # 'kadcar_Material.005.glb',
    # 'kadcar_Material.007.glb',
    # 'kadcar_Material.010.glb',
    # 'kadcar_Material.011.glb',
    # 'kadcar_Material.014.glb',
    # 'kadcar_Material.015.glb'
]

import_background_into_scene(os.path.join(path_to_glb_folder, 'mtn_no_car.glb'), 'bg')
import_scene_into_collection(os.path.join(path_to_glb_folder, 'blue_aligned_empty.glb'), 'car')
import_scene_into_collection(os.path.join(path_to_glb_folder, 'rim_skinny.glb'), 'rims')
# move_collection_to_location('car', {'x': 0, 'y': 0, 'z':0.0}, {'w': 1.0, 'x':0.0, 'y':0.0, 'z':0.0})

#1: select car as collection
deselect_all_scene_objects()
bpy.ops.object.select_same_collection(collection='car')
#2: transform car by z
for o in bpy.context.selected_objects:
    if o.name == 'Kadcar_Empty':
        o.location.x = 0.0
        o.location.y = -1.69032
        o.location.z = 0.0
        
        o.rotation_quaternion.w = 0.716793
        o.rotation_quaternion.x = 0.0
        o.rotation_quaternion.y = 0.0
        o.rotation_quaternion.z = 0.697286

        replace_object(True, True, o.name, 'rim_front_right.001')
        replace_object(True, True, o.name, 'rim_front_left.001')
        replace_object(True, True, o.name, 'rim_back_right.001')
        replace_object(True, True, o.name, 'rim_back_left.001')

set_scene_camera(cam_name="Camera")
configure_render_settings('CYCLES', 'CUDA', 'GPU', 200, 50)
set_render_output_settings(path_to_glb_folder, 'WEBP', True)
bpy.ops.object.select_all(action="SELECT")
kfile = os.path.join(path_to_glb_folder, 'something_else.glb')
export_scene_as_gltf(kfile)
print(bpy.data.objects.get('rim_front_right').location.y)
