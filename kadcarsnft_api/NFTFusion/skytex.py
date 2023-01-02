import os
import bpy
from scene_utils import customize_world_shader_nodes, import_scene_into_collection, export_scene_as_gltf
from render_utils import *
from pygltflib import GLTF2
from pygltflib.utils import gltf2glb

dirname = os.path.dirname(__file__)
path_to_assets_folder = os.path.join(dirname, 'assets')
path_to_background_config = os.path.join(dirname, 'background_config_files')

# customize_world_shader_nodes(os.path.join(path_to_assets_folder, "hdr_files/snow_background.hdr"), 'HDRI')
# customize_world_shader_nodes(os.path.join(path_to_assets_folder, "hdr_files/snow_background.hdr"), 'cyber')
configure_render_settings('CYCLES', 'CUDA', 'CPU', 20, 10)
set_render_output_settings(os.path.join(dirname, "lolol"), 'WEBP', 2163, 1403, True)



# import_scene_into_collection(os.path.join(path_to_assets_folder, "kadcars/k2.glb"), "car")
# export_scene_as_gltf(os.path.join(dirname, "testing.gltf"), True, 'GLTF_EMBEDDED')

# gltf = GLTF2()
# gltf = gltf.load(os.path.join(dirname, "testing.gltf"))
# gltf.extras = {"lol":"haha"}
# gltf.save(os.path.join(dirname, "testing.gltf"))
# gltf2glb(os.path.join(dirname, "testing.gltf"), os.path.join(dirname, "testing.glb"), override=True)


# glb = GLTF2().load(os.path.join(dirname, "testing.glb"))
# print(glb.extras)