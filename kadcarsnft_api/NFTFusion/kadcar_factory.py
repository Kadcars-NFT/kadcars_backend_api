import os
import bpy
import json
from scene_utils import delete_all_objects, export_scene_as_gltf, get_objects_from_collection_by_names, select_only_objects_in_collection
from shader_utils import transfer_materials_bulk
from shader_utils import transfer_materials
from scene_utils import deselect_all_scene_objects, import_scene_into_collection, parenting_object
from bpy_data_utils import rename_object_in_scene
from io_utils import extract_data_from_json

#Method to add color to specified portion of kadcar
def colorize_kadcar(part_name, colorset, material_name):
    file = open('car_parts.json')
    file_data = json.load(file)
    car_part_components = file_data[part_name]
    
    color_file = open("colors.json")
    color_data = json.load(color_file)[colorset]

    for color in color_data:
        material = bpy.data.materials[material_name]
        material.use_nodes = True
        tree = material.node_tree
        nodes = tree.nodes
        bsdf = nodes["Principled BSDF"]
        print(bsdf.inputs)

        print(color)
        print(color_data)
        color_obj = color_data[color]
        bsdf.inputs["Base Color"].default_value = (color_obj['r'], color_obj['g'], color_obj['b'], color_obj['a'])
        # material.diffuse_color = (0,0,0,0)

        #Apply material to every part of the kadcar
        for comp in car_part_components:
            template_object = bpy.data.objects.get(comp)
            # template_object.material_slots[0].link = 'OBJECT'
            
            # #create material to add color here
            # material = bpy.data.materials.new("TEST")
            # material.use_nodes = True
            # tree = material.node_tree
            # nodes = tree.nodes
            # bsdf = nodes["Principled BSDF"]
            # bsdf.inputs["Base Color"].default_value = (0, 1, 0, 0.8)
            # material.diffuse_color = (0,1,0,0.8)

            # #apply color here
            # ob = template_object.copy()
            # ob.active_material = material
            template_object.active_material = material
            bpy.context.collection.objects.link(template_object)

def add_materials_to_kadcar(kadcar_gltf_path, car_part_objects, kc_name, format='glb'):
    # material_list = ['steel', 'metallic', 'grainy1', 'darker', 'matte', 'standard']
    material_list = ['steel']
    dirname = os.path.dirname(__file__)
    # material_file = os.path.join(dirname, 'assets/material_spheres.glb')
    material_file = os.path.join(dirname, 'assets/material_spheres_new.glb')

    materials_collection = import_scene_into_collection(material_file, 'materials')
    kadcar_collection = import_scene_into_collection(kadcar_gltf_path, 'kadcar')

    glb_file_names = []

    for obj in materials_collection.all_objects:
        if obj.type == 'MESH':
            print(obj.name)
            if obj.name.split('.')[0] not in material_list:
                continue

            file_name = kc_name.split(".")[0] + obj.name.split('.')[0] + obj.name.split('.')[1] + '.' + format
            transfer_materials_bulk(clean=True, src=obj, target_object_names=car_part_objects)
            select_only_objects_in_collection(kadcar_collection)
            export_scene_as_gltf(os.path.join(dirname, 'assets/with_shading/' + file_name), export_all=False)
            glb_file_names.append(file_name)
    
    return glb_file_names

def add_rims_to_kadcar(kadcar_gltf_path, rim_gltf_path):
    import_scene_into_collection(kadcar_gltf_path, 'kadcar')
    import_scene_into_collection(rim_gltf_path, 'rims')
    
    dirname = os.path.dirname(__file__)
    car_parts_json = os.path.join(dirname, 'car_parts.json')
    rim_object_names = extract_data_from_json(car_parts_json)['rims']
    
    deselect_all_scene_objects()
    old_names = []
    for rim_name in rim_object_names:
        old_names.append(rim_name)
        rim = bpy.data.objects[rim_name]
        rim.select_set(True)
        bpy.data.objects.remove(rim, do_unlink=True)
        # bpy.ops.object.delete()

    #TODO CRITICAL: rename rims properly
    place_object(False, False, 'Kadcar_Empty', 'rim_front_right.001')
    place_object(False, False, 'Kadcar_Empty', 'rim_front_left.001')
    place_object(False, False, 'Kadcar_Empty', 'rim_back_right.001')
    place_object(False, False, 'Kadcar_Empty', 'rim_back_left.001')

    rename_object_in_scene('rim_front_right.001', 'rim_front_right')
    rename_object_in_scene('rim_front_left.001', 'rim_front_left')
    rename_object_in_scene('rim_back_right.001', 'rim_back_right')
    rename_object_in_scene('rim_back_left.001', 'rim_back_left')

    deselect_all_scene_objects()

#TODO: rename replaced object
def replace_object(should_transfer_w_materials, should_clear_old_materials, dest_group_object_name, target_name):
    dest_group_object = bpy.data.objects.get(dest_group_object_name)
    target_object = bpy.data.objects.get(target_name)

    target_object.location.x = dest_group_object.location.x
    target_object.location.y = dest_group_object.location.y
    target_object.location.z = dest_group_object.location.z

    target_object.rotation_quaternion.w = dest_group_object.rotation_quaternion.w
    target_object.rotation_quaternion.x = dest_group_object.rotation_quaternion.x
    target_object.rotation_quaternion.y = dest_group_object.rotation_quaternion.y
    target_object.rotation_quaternion.z = dest_group_object.rotation_quaternion.z

    bpy.ops.object.select_all(action="DESELECT")
    
    target_object.select_set(True)
    bpy.context.view_layer.objects.active = target_object
    bpy.ops.object.transform_apply(location=True, rotation=True)

    parenting_object(dest_group_object, target_object)

    if should_transfer_w_materials:
        transfer_materials(should_clear_old_materials, dest_group_object, target_object)

def place_object(should_transfer_w_materials, should_clear_old_materials, dest_group_object_name, target_name):
    dest_group_object = bpy.data.objects.get(dest_group_object_name)
    target_object = bpy.data.objects.get(target_name)

    target_object.location.x = dest_group_object.location.x
    target_object.location.y = dest_group_object.location.y
    target_object.location.z = dest_group_object.location.z

    target_object.rotation_quaternion.w = dest_group_object.rotation_quaternion.w
    target_object.rotation_quaternion.x = dest_group_object.rotation_quaternion.x
    target_object.rotation_quaternion.y = dest_group_object.rotation_quaternion.y
    target_object.rotation_quaternion.z = dest_group_object.rotation_quaternion.z

    bpy.ops.object.select_all(action="DESELECT")

    target_object.select_set(True)
    bpy.context.view_layer.objects.active=target_object
    bpy.ops.object.transform_apply(location=True, rotation=True)

    parenting_object(dest_group_object, target_object)

    if should_transfer_w_materials:
        transfer_materials(should_clear_old_materials, dest_group_object, target_object)

def apply_color_to_windshield(color):
    pass

def customize_kadcar_hood(material_name):
    pass

def apply_decal_to_kadcar(decal):
    pass


def generate_kadcar_gltfs(materials_file, kadcar_file, format='glb'):
    delete_all_objects()
    material_collection = import_scene_into_collection(materials_file, 'materials')

    #Prep car
    car_collection = import_scene_into_collection(kadcar_file, 'car')
    
    f = open('car_parts.json')
    data = json.load(f)
    car_parts = data["body"]
    f.close()

    car_part_objects = get_objects_from_collection_by_names(car_collection, car_parts)

    glb_file_names = []

    for obj in material_collection.all_objects:
        if obj.type == 'MESH':
            file_name = 'kadcar_' + obj.name + '.' + format
            print("type: "+obj.type+"   material: "+obj.material_slots[0].name )
            transfer_materials_bulk(clean=True, src=obj, target_object_names=car_part_objects)
            select_only_objects_in_collection(car_collection)
            export_scene_as_gltf(file_name)
            glb_file_names.append(file_name)
            bpy.ops.wm.read_factory_settings(use_empty=True)

    delete_all_objects()
    return glb_file_names