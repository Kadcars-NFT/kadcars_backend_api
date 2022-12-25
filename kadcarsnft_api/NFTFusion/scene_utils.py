import bpy
import json
import math
import os
from io_utils import extract_data_from_json

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

def clear_scene_except_cameras():
    bpy.ops.object.select_all(action='SELECT')
    for o in bpy.context.selected_objects:
        if o.type == "CAMERA":
            o.select_set(False)
    bpy.ops.object.delete()

def set_car_location_in_scene(filepath, location, rotation_quaternion):
    # delete_all_objects()
    # bpy.ops.import_scene.gltf(filepath=filepath)
    # collection_name = 'car'
    # bpy.ops.collection.create(name=collection_name)
    deselect_all_scene_objects()
    import_scene_into_collection(filepath, 'kadcar')

    # move_collection_to_location('kadcar', location, rotation_quaternion)
    move_kadcar(location, rotation_quaternion)

def move_kadcar(location, rotation_quaternion):
    obj = bpy.data.objects['Kadcar_Empty']
    print(obj.name)
    obj.location.x = location['x']
    obj.location.y = location['y']
    obj.location.z = location['z']

    obj.rotation_quaternion.w = rotation_quaternion['w']
    obj.rotation_quaternion.x = rotation_quaternion['x']
    obj.rotation_quaternion.y = rotation_quaternion['y']
    obj.rotation_quaternion.z = rotation_quaternion['z']
    print(obj.location)
    print(obj.rotation_quaternion)

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
def customize_world_shader_nodes(hdri, type='HDRI'):
    context = bpy.context
    scene = context.scene

    #Get the environment node tree of the current scene
    node_tree = scene.world.node_tree
    tree_nodes = node_tree.nodes
    links = node_tree.links

    #Clear all nodes
    tree_nodes.clear()

    #Add background node
    node_background = tree_nodes.new(type='ShaderNodeBackground')
    node_background.inputs['Strength'].default_value = 3.5
    
    #Add output node
    node_output = tree_nodes.new(type='ShaderNodeOutputWorld')
    node_output.location = 200,0

    if type == 'HDRI':
        #Add environment texture node
        node_environment = tree_nodes.new('ShaderNodeTexEnvironment')

        #Load and assign the image to then node property
        node_environment.image = bpy.data.images.load(hdri)
        node_environment.location = -300, 0
    
        #Link all nodes
        # links = node_tree.links
        links.new(node_environment.outputs["Color"], node_background.inputs["Color"])
        links.new(node_background.outputs["Background"], node_output.inputs["Surface"])

    elif type == 'SKY':
        sky_texture = tree_nodes.new('ShaderNodeTexSky')
        mapping_node = tree_nodes.new('ShaderNodeMapping')
        tex_coord_node = tree_nodes.new('ShaderNodeTexCoord')

        #Customize sky texture
        sky_texture.sky_type = 'NISHITA'
        sky_texture.sun_disc = False
        sky_texture.sun_elevation = math.radians(24)
        sky_texture.sun_rotation = math.radians(-212.0)
        sky_texture.air_density = 3.0
        sky_texture.dust_density = 10.0
        sky_texture.ozone_density = 6.0

        #Customize mapping node
        mapping_node.vector_type = "POINT"
        mapping_node.inputs["Rotation"].default_value = (math.radians(-10.5), math.radians(6.1), math.radians(272.0))

        tex_coord_node.from_instancer = True

        #Link nodes
        links.new(tex_coord_node.outputs["Generated"], mapping_node.inputs["Vector"])
        links.new(mapping_node.outputs["Vector"], sky_texture.inputs["Vector"])
        links.new(sky_texture.outputs["Color"], node_background.inputs["Color"]) #connect sky texture to background node
        links.new(node_background.outputs["Background"], node_output.inputs["Surface"]) #connect background node to world node

def import_background_into_scene(filepath, collection_name, hdri=None):
    deselect_all_scene_objects()
    import_scene_into_collection(filepath, collection_name)
    set_scene_camera(cam_name="Camera")

    if hdri:
        customize_world_shader_nodes(hdri)

def import_scene_into_collection(filepath, collection_name):
    deselect_all_scene_objects()
    
    if collection_name in bpy.data.collections:
        if bpy.data.collections[collection_name] is not bpy.context.scene.collection:
            bpy.data.collections.remove(bpy.data.collections[collection_name])

    bpy.ops.import_scene.gltf(filepath=filepath)
    bpy.ops.collection.create(name=collection_name)

    return bpy.data.collections[collection_name]

def set_scene_camera(cam_name):
    obj_camera = bpy.data.objects[cam_name]
    bpy.context.scene.camera = obj_camera

#Changes camera using metadata
def apply_changes_to_scene_camera(camera_metadata):
    pass

#Creates new camera using metadata and adds it to the scene
def add_new_camera_to_scene(camera_metadata):
    pass

def relink_collection(src_collection_name, dest_collection_name):
    src_collection = bpy.data.collections[src_collection_name]
    dest_collection = bpy.data.collections[dest_collection_name]

    for o in src_collection.all_objects:
        dest_collection.objects.link(o)
        src_collection.objects.unlink(o)

def delete_all_objects_in_scene():
    bpy.ops.outliner.orphans_purge()
    bpy.ops.object.select_all(action='SELECT')
    delete_and_unlink()
    
    # for collection in bpy.data.collections:
    #     if collection != "Collection":
    #         bpy.data.collections.remove(collection)
    # bpy.ops.object.delete()

def delete_objects_from_collection_name(collection_name):
    bpy.ops.outliner.orphans_purge()
    select_only_objects_in_collection_name(collection_name)
    delete_and_unlink()
    # bpy.ops.object.delete()

def delete_objects_from_collection(collection):
    bpy.ops.outliner.orphans_purge()
    select_only_objects_in_collection(collection)
    delete_and_unlink()
    # bpy.ops.object.delete()

def delete_and_unlink():
    for o in bpy.context.selected_objects:
        bpy.data.objects.remove(o, do_unlink=True)

def select_only_objects_in_collection_name(collection_name):
    collection = bpy.data.collections[collection_name]
    deselect_all_scene_objects()
    select_all_objects_in_collection(collection)

def select_only_objects_in_collection(collection):
    deselect_all_scene_objects()
    select_all_objects_in_collection(collection)

def deselect_all_scene_objects():
    # for ob in bpy.context.selected_objects:
    #     ob.select_set(False)
    bpy.ops.object.select_all(action='DESELECT')

def select_all_objects_in_scene():
    for scene in bpy.data.scenes:
        for view_layer in scene.view_layers:
            for o in view_layer.objects:
                print(o.users_collection[0].name)

def select_all_objects_in_collection(collection):
    # for obj in collection.all_objects:
    #     obj.select_set(True)
    for scene in bpy.data.scenes:
        for view_layer in scene.view_layers:
            for o in view_layer.objects:
                if o.users_collection[0].name == collection.name:
                    o.select_set(True)

def get_objects_from_collection_by_names(collection, name_list):
    object_list = []
    for obj in collection.all_objects:
        if obj.name in name_list:
            object_list.append(obj)

    return object_list

def parenting_object(parent_object, child_object):
    bpy.ops.object.select_all(action="DESELECT")
    child_object.select_set(True)
    parent_object.select_set(True)
    bpy.context.view_layer.objects.active = parent_object
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

def add_lights_to_scene(lights_config, file_prefix):
    lights_data = extract_data_from_json(os.path.join(file_prefix, lights_config))
    lights = lights_data["lights"]

    for light in lights:
        name = light["name"]
        light_data = bpy.data.lights.new(name=name, type=light["type"])
        light_data.energy = light["energy"]

        light_object = bpy.data.objects.new(name=name+'_obj', object_data=light_data)

        bpy.context.collection.objects.link(light_object)

        light_object.location = light["location"]
        light_object.rotation_euler = light["rotation_euler"]
        light_object.scale = light["scale"]

def export_scene_as_gltf(output_file, export_all=True):
    filepath = 'C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/'
    # filepath = '/usr/src/app/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets'
    
    if export_all:
        bpy.ops.object.select_all(action="SELECT")

    bpy.ops.export_scene.gltf(
        filepath=os.path.join(filepath, output_file),
        use_selection=True,
        export_apply=True,
        export_texcoords=True,
        export_normals=True,
        export_tangents=True,
        export_materials='EXPORT',
        export_colors=True,
        export_cameras=export_all,
        export_animations=False
        # use_mesh_edges=True,
        # use_mesh_vertices=True,
        # export_extras=True
    )
