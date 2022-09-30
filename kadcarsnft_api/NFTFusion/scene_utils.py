import bpy
import json

#Cleans up scene by deleting all objects
def delete_all_objects():
    """
    Deletes all objects in the current scene
    """
    deleteListObjects = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'HAIR', 'POINTCLOUD', 'VOLUME', 'GPENCIL',
                         'ARMATURE', 'LATTICE', 'EMPTY', 'LIGHT', 'LIGHT_PROBE', 'CAMERA', 'SPEAKER']

    # Select all objects in the scene to be deleted:

    for o in bpy.context.scene.objects:
        for i in deleteListObjects:
            if o.type == i:
                o.select_set(False)
            else:
                o.select_set(True)
    bpy.ops.object.delete() # Deletes all selected objects in the scene

#Creates light object using given light metadata and adds it to the scene
def create_area_light_object(light_metadata):
    bpy.ops.object.light_add(
        type='AREA', 
        # radius=light_metadata['radius'], 
        align=light_metadata['align'],
        location=light_metadata['location'], 
        rotation=light_metadata['rotation'], 
        scale=light_metadata['scale']
    )
    light_ob = bpy.context.object
    light = light_ob.data

    light.energy = light_metadata['energy']
    light.color = light_metadata['color']
    light.shape = light_metadata['shape']

    # light.diffuse = light_metadata['diffuse_factor']
    light.specular_factor = light_metadata['specular_factor']
    # light.volume_factor = light_metadata['volume_factor']

    if light_metadata['shape'] == 'RECTANGLE':
        light.size = light_metadata['size']
        light.size_y = light_metadata['size_y']

#Applies given HDRI background to scene
def apply_hdri(hdri):
    context = bpy.context
    scene = context.scene

    #Get the environment node tree of the current scene
    node_tree = scene.world.node_tree
    tree_nodes = node_tree.nodes

    #Clear all nodes
    tree_nodes.clear()

    #Add background node
    node_background = tree_nodes.new(type='ShaderNodeBackground')

    #Add environment texture node
    node_environment = tree_nodes.new('ShaderNodeTexEnvironment')

    #Load and assign the image to then node property
    node_environment.image = bpy.data.images.load(hdri)
    node_environment.location = -300, 0

    #Add output node
    node_output = tree_nodes.new(type='ShaderNodeOutputWorld')
    node_output.location = 200,0

    #Link all nodes
    links = node_tree.links
    link = links.new(node_environment.outputs["Color"], node_background.inputs["Color"])
    link = links.new(node_background.outputs["Background"], node_output.inputs["Surface"])

#Changes camera using metadata
def apply_changes_to_scene_camera(camera_metadata):
    pass

#Creates new camera using metadata and adds it to the scene
def add_new_camera_to_scene(camera_metadata):
    pass