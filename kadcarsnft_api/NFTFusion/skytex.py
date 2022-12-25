import os
import bpy
from scene_utils import customize_world_shader_nodes
from render_utils import *

dirname = os.path.dirname(__file__)
path_to_assets_folder = os.path.join(dirname, 'assets')
path_to_background_config = os.path.join(dirname, 'background_config_files')

# customize_world_shader_nodes(os.path.join(path_to_assets_folder, "hdr_files/snow_background.hdr"), 'HDRI')
# customize_world_shader_nodes(os.path.join(path_to_assets_folder, "hdr_files/snow_background.hdr"), 'SKY')
# configure_render_settings('CYCLES', 'CUDA', 'CPU', 20, 10)
# set_render_output_settings(os.path.join(dirname, "lolol"), 'WEBP', True)


context = bpy.context
scene = context.scene

#Get the environment node tree of the current scene
node_tree = scene.world.node_tree
tree_nodes = node_tree.nodes
links = node_tree.links

#Clar all nodes
tree_nodes.clear()

#Add background node
node_background = tree_nodes.new(type='ShaderNodeBackground')