import bpy
import json
import os

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
    deselect_all_scene_objects()
    bpy.ops.import_scene.gltf(filepath=filepath)
    collection_name = 'car'
    bpy.ops.collection.create(name=collection_name)

    move_collection_to_location(collection_name, location, rotation_quaternion)

def move_collection_to_location(collection_name, location, rotation_quaternion):
    target_col = bpy.data.collections[collection_name]
    for obj in target_col.all_objects:
        # print("name: " + obj.name + "     type: " + obj.type)
        #TODO: fix object types
        if obj.type == 'MESH':
            obj.location.x = location['x']
            obj.location.y = location['y']
            obj.location.z = location['z']

            obj.rotation_quaternion.w = rotation_quaternion['w']
            obj.rotation_quaternion.x = rotation_quaternion['x']
            obj.rotation_quaternion.y = rotation_quaternion['y']
            obj.rotation_quaternion.z = rotation_quaternion['z']


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

def import_background_into_scene(filepath, collection_name, hdri=None):
    deselect_all_scene_objects()
    import_scene_into_collection(filepath, collection_name)
    set_scene_camera(cam_name="Camera")

    if hdri:
        apply_hdri(hdri)

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

def delete_objects_from_collection_name(collection_name):
    select_only_objects_in_collection_name(collection_name)
    bpy.ops.object.delete()

def delete_objects_from_collection(collection):
    select_only_objects_in_collection(collection)
    bpy.ops.object.delete()

def delete_all_objects_in_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

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

def select_all_objects_in_collection(collection):
    # for obj in collection.all_objects:
    #     obj.select_set(True)
    for scene in bpy.data.scenes:
        for view_layer in scene.view_layers:
            for o in view_layer.objects:
                if o.users_collection[0].name == collection.name:
                    print(o.users_collection[0].name)
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
        #TODO: bpy version
        # use_mesh_edges=True,
        # use_mesh_vertices=True,
        # export_extras=True
    )
