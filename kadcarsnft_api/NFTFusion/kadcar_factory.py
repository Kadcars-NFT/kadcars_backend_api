import os
import bpy
import json
from scene_utils import *
from shader_utils import transfer_materials, transfer_materials_bulk, get_material_for_given_car_part
from scene_utils import deselect_all_scene_objects, import_scene_into_collection, parenting_object
from bpy_data_utils import rename_object_in_scene
from io_utils import extract_data_from_json, extract_json_attribute_data

def add_materials_to_kadcar(kadcar_gltf_path, car_part_objects, kc_name, format='glb'):
    # material_list = ['steel', 'metallic', 'grainy1', 'darker', 'matte', 'standard']
    material_list = ['steel']
    dirname = os.path.dirname(__file__)

    material_file = os.path.join(dirname, 'assets/material_spheres_new.glb')
    # material_file = os.path.join(dirname, 'assets/material_spheres_red.glb')

    materials_collection = import_scene_into_collection(material_file, 'materials')
    kadcar_collection = import_scene_into_collection(kadcar_gltf_path, 'kadcar')

    glb_file_names = []

    count = {
        'steel' : 0,
        # 'metallic': 0,
        # 'matte': 0,
        # 'grainy1': 0,
        # 'darker': 0,
        # 'standard': 0
    }

    for obj in materials_collection.all_objects:
        if obj.type == 'MESH':
            print(obj.name)
            material_type = obj.name.split('.')[0]
            
            #CHECK MATERIAL TYPE COMMENTED FOR TESTING

            # if material_type not in material_list:
            #     continue

            # if material_type in count.keys():
            #     if count[material_type] == 1:
            #         continue
            #     count[material_type] += 1

            file_name = kc_name.split(".")[0] + obj.name.split('.')[0] + obj.name.split('.')[1] + '.' + format
            transfer_materials_bulk(clean=True, src=obj, target_object_names=car_part_objects)
            select_only_objects_in_collection(kadcar_collection)
            export_scene_as_gltf(os.path.join(dirname, 'assets/with_shading/' + file_name), export_all=False)
            glb_file_names.append(file_name)

    return glb_file_names

def add_material_and_colorize_kadcar(filepath_prefix, kadcar_specs):
    parts_to_colorize = [str('colorize-' + kadcar_specs['Kadcar']), "emblem", "headlights", "rims", "seats", "hood_trim", "grill_outer", "grill_inner"]

    colorize_data = extract_data_from_json('colorize.json')

    for part in parts_to_colorize:
        components_to_colorize = colorize_data[part]
        material_name = get_material_for_given_car_part(kadcar_specs, part)
        add_material_and_colorize_components(filepath_prefix, components_to_colorize, material_name)

def add_material_and_colorize_components(filepath_prefix, car_part_objects, material_name):
    material_file = os.path.join(filepath_prefix, 'material_spheres_new.glb')

    import_scene_into_collection(material_file, 'materials')
    
    material = bpy.data.objects[material_name]

    transfer_materials_bulk(clean=True, src=material, target_object_names=car_part_objects)

def add_rims_to_kadcar(rim_gltf_path):
    import_scene_into_collection(rim_gltf_path, 'rims')
    
    # dirname = os.path.dirname(__file__)
    # car_parts_json = os.path.join(dirname, 'car_parts.json')
    # rim_object_names = extract_data_from_json(car_parts_json)['rims']
    rim_object_names = extract_json_attribute_data('car_parts.json', 'rims')
    deselect_all_scene_objects()

    old_names = []
    for rim_name in rim_object_names:
        old_names.append(rim_name)
        rim = bpy.data.objects[rim_name]
        rim.select_set(True)
        bpy.data.objects.remove(rim, do_unlink=True)
        bpy.ops.outliner.orphans_purge()
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
    relink_collection('rims', 'kadcar')

def add_spoiler_to_kadcar(kadcar_specs, spoiler_gltf_path):
    if kadcar_specs['Spoiler'] == 'k2p':
        return

    import_scene_into_collection(spoiler_gltf_path, 'spoilers')

    dirname = os.path.dirname(__file__)
    car_parts_json = os.path.join(dirname, 'car_parts.json')
    spoiler_obj_name = extract_data_from_json(car_parts_json)['spoiler']

    deselect_all_scene_objects()
    old_names = []
    for spoiler_name in spoiler_obj_name:
        print(spoiler_name)
        old_names.append(spoiler_name)
        spoiler = bpy.data.objects[spoiler_name]
        spoiler.select_set(True)
        bpy.data.objects.remove(spoiler, do_unlink=True)
        bpy.ops.outliner.orphans_purge()

    place_object(False, False, 'Kadcar_Empty', 'spoiler.001')
    rename_object_in_scene('spoiler.001', 'spoiler')

    deselect_all_scene_objects()
    relink_collection('spoilers', 'kadcar')

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

def build_car_metadata(kadcar_specs):
    kadcar_export_file_name = str(
        kadcar_specs['Kadcar'] + "_" + kadcar_specs['Rim'] + "_" +
        kadcar_specs['Spoiler'] + "_" + kadcar_specs['Trim'] + "_" + 
        kadcar_specs['Color'] + "_" + kadcar_specs['Material'] + "_" + 
        kadcar_specs['Background']
    )

    metadata = {
        "kadcar": kadcar_specs['Kadcar'],
        "rim": kadcar_specs['Rim'],
        "spoiler": kadcar_specs['Spoiler'],
        "trim": kadcar_specs['Trim'],
        "color": kadcar_specs['Color'],
        "material": kadcar_specs['Material'],
        "background": kadcar_specs['Background']
    }

    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, "metadata_json/" + kadcar_export_file_name + ".json"), "w") as outfile:
        json.dump(metadata, outfile)

    return kadcar_export_file_name

def apply_color_to_windshield(color):
    pass

def customize_kadcar_hood(material_name):
    pass

def apply_decal_to_kadcar(decal):
    pass