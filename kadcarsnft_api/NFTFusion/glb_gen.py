import os
import bpy
from NFT_render_provider import *
from scene_utils import *
from io_utils import *
from kadcar_factory import *
from generators import *

scene_names = ['BEACH', 'MOUNTAIN', 'SNOW']

dirname = os.path.dirname(__file__)
path_to_glb_folder = os.path.join(dirname, 'assets')
path_to_jpeg_folder = os.path.join(dirname, 'assets')

materials_file = os.path.join(path_to_glb_folder, 'material_cubes.glb')
kadcar_file = os.path.join(path_to_glb_folder, 'aligned_renamed_rims.glb')

#create kadcar glbs with customization
# kc_glb_list = generate_kadcar_gltfs(materials_file, kadcar_file, 'glb')
kc_glb_list = [
    '00darker001.glb',
    '00grainy1001.glb',
    '00matte002.glb',
    '00metallic003.glb',
    '00standard001.glb',
    '00steel001.glb'
]
delete_all_objects_in_scene()
generate_scenes_w_kadcar_and_background_gltfs(kc_glb_list, path_to_glb_folder)