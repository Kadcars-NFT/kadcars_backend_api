import os
import bpy
from kadcar_factory import generate_kadcar_gltfs
from NFT_render_provider import *
from scene_utils import *


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
    'kadcar_Material.002.glb',
    'kadcar_Material.003.glb',
    # 'kadcar_Material.005.glb',
    # 'kadcar_Material.005.glb',
    # 'kadcar_Material.007.glb',
    # 'kadcar_Material.010.glb',
    # 'kadcar_Material.011.glb',
    # 'kadcar_Material.014.glb',
    # 'kadcar_Material.015.glb'
]

car_coll = import_scene_into_collection(filepath=os.path.join(path_to_glb_folder, "blue_aligned_empty.glb"), collection_name='car')
import_scene_into_collection(filepath=os.path.join(path_to_glb_folder, "material_spheres.glb"), collection_name='material')

for o in bpy.context.selected_objects:
    print(o.users_collection[0].name)

obj_camera = bpy.data.objects["Camera"]
bpy.context.scene.camera = obj_camera
select_only_objects_in_collection(car_coll)
clear_scene_except_cameras()
export_scene_as_gltf("hahaha.glb", export_all=False)
# for o in bpy.data.collections['car'].all_objects:
#     print("Name: " + o.name + "              Type: " + o.type)
#     o.select_set(True)

# for scene in bpy.data.scenes:
#     for view_layer in scene.view_layers:
#         print(view_layer)
#         for o in view_layer.objects:
#             print(o.name + "     " + o.users_collection[0].name)
#             o.select_set(True)
# for scene in scene_names:
#     if scene == 'BEACH':
#         pass
#     elif scene == 'MOUNTAIN':
#         generate_kadcar_nft_with_mountain_bg_old(path_to_glb_folder, kc_glb_list)
#     elif scene == 'SNOW':
#         pass