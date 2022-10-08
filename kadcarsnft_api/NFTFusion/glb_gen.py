import os
import bpy
from kadcar_factory import generate_kadcar_gltfs
from NFT_render_provider import *
from scene_utils import delete_all_objects

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

for scene in scene_names:
    if scene == 'BEACH':
        pass
    elif scene == 'MOUNTAIN':
        generate_kadcar_ft_with_mountain_bg(path_to_glb_folder, kc_glb_list)
    elif scene == 'SNOW':
        pass