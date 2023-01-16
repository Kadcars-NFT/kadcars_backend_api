import os
import bpy
import json
from scene_utils import *
from shader_utils import get_material_for_given_car_part, transfer_materials_bulk, transfer_materials, apply_texture_image_to_object, change_object_base_color, change_object_emission_level
from scene_utils import deselect_all_scene_objects, import_scene_into_collection, parenting_object
from bpy_data_utils import rename_object_in_scene
from io_utils import extract_data_from_json, extract_json_attribute_data
from stat_dictionaries import *
from nft_metadata_handler import update_cosmetic_type_and_id_in_mutable_state

def add_materials_and_colorize_kadcar(filepath_prefix, kadcar_specs, kadcar_metadata):
    #Add material spheres to scene
    dirname = os.path.dirname(__file__)
    material_file = os.path.join(filepath_prefix, 'material_gltfs/material_spheres_new.glb')
    import_scene_into_collection(material_file, 'materials')

    #Extract car part colorization data
    colorize_data = extract_data_from_json(os.path.join(dirname, 'json_config_files/colorize.json'))
    primary_color_independent = colorize_data["independent"]
    primary_color_dependent = colorize_data["dependent"]

    #Apply trim to kadcar
    add_trim_to_kadcar(filepath_prefix, kadcar_specs['Trim'], kadcar_metadata, kadcar_specs)

    add_headlight_panels_to_kadcar(filepath_prefix, kadcar_specs)

    #Add color and material to body
    add_material_and_colorize_components(primary_color_independent['body'], str(kadcar_specs['Material'] + "-" + kadcar_specs['Color']))
    # update_cosmetic_type_and_id_in_mutable_state(kadcar_metadata["mutable-state"]["components"], kadcar_specs, "body", 'material', kadcar_specs['Material'] + "-" + feature_names['colors'][kadcar_specs['Color']])

    #Change headlight color
    change_kadcar_headlight_color(kadcar_metadata, kadcar_specs)

    #Get materials for dependent groups
    for part in primary_color_dependent:
        components_to_colorize = primary_color_dependent[part]["objects"]
        material_name = get_material_for_given_car_part(kadcar_specs, part)

        material_metadata_name = material_name
        if material_name.split('-')[0] == 'steel':
            material_metadata_name = 'matte metallic-' + material_name.split('-')[1]

        update_cosmetic_type_and_id_in_mutable_state(kadcar_metadata["mutable-state"]["components"], kadcar_specs, part, 'material', material_metadata_name)

        if material_name == "default":
            continue
        add_material_and_colorize_components(components_to_colorize, material_name)

    return kadcar_metadata

def add_material_and_colorize_components(car_part_objects, material_name):
    material = bpy.data.objects[material_name]
    transfer_materials_bulk(clean=True, src=material, target_object_names=car_part_objects)

def apply_paint_job_to_kadcar_body_from_presets(filepath_prefix, primary_color_independent, kadcar_specs, kadcar_metadata):
    add_material_and_colorize_components(primary_color_independent['body'], str(kadcar_specs['Material'] + "-" + kadcar_specs['Color']))
    update_cosmetic_type_and_id_in_mutable_state(kadcar_metadata["mutable-state"]["components"], kadcar_specs, "body", 'material', feature_names['colors'][kadcar_specs['Color']])

def add_trim_to_kadcar(filepath_prefix, trim_type, kadcar_metadata, kadcar_specs):
    trim_object = bpy.data.objects['Car_Trim']
    stat_type = ""
    
    if trim_type == 'steel':
        stat_type = "material"
        src_material = bpy.data.objects['steel-lightgray']
        transfer_materials(clean=True, src=src_material, tgt=trim_object)
    elif trim_type == 'chrome':
        stat_type = "material"
        src_material = bpy.data.objects['chrome']
        transfer_materials(clean=True, src=src_material, tgt=trim_object)
    else:
        stat_type = "texture"
        apply_texture_image_to_object(True, os.path.join(filepath_prefix, 'trims/' + trim_type + '.jpg'), trim_object)

    update_cosmetic_type_and_id_in_mutable_state(kadcar_metadata["mutable-state"]["components"], kadcar_specs, 'trim', stat_type, feature_names['trims'][trim_type])

def change_kadcar_headlight_color(kadcar_metadata, kadcar_specs):
    headlight_object = bpy.data.objects['Headlights']
    color_name = ""
    color_vector = None

    # if kadcar_specs['Spoiler'] == 'spoiler_1' or kadcar_specs['Spoiler'] == 'clearance_light_1':
    if kadcar_specs['Headlights'] == 'white':
        color_name = "white"
        color_vector = [1.0, 1.0, 1.0, 1.0]
        change_object_base_color(color_vector, 'headlight_color', headlight_object) #White headlights
    # elif kadcar_specs['Spoiler'] == 'spoiler_2' or kadcar_specs['Spoiler'] == 'clearance_light_2':
    elif kadcar_specs['Headlights'] == 'orange':
        color_name = "orange"
        color_vector = [1.0, 0.143401, 0.001641, 1.0]
        change_object_base_color(color_vector, 'headlight_color', headlight_object) #Orange headlights
    
    change_object_emission_level(headlight_object, 12.5, color_vector)
    update_cosmetic_type_and_id_in_mutable_state(kadcar_metadata["mutable-state"]["components"], kadcar_specs, 'headlights', 'material', color_name)

def add_headlight_panels_to_kadcar(filepath_prefix, kadcar_specs):
    if kadcar_specs['Headlight_Panels'] == 'grated':
        return

    import_scene_into_collection(os.path.join(filepath_prefix, 'headlight_panels/' + kadcar_specs['Headlight_Panels'] + ".glb"), 'headlight_panels')

    headlight_panels = bpy.data.objects['Metal_Sheet']
    headlight_panels.select_set(True)
    bpy.data.objects.remove(headlight_panels, do_unlink=True)
    bpy.ops.outliner.orphans_purge()

    deselect_all_scene_objects()
    place_object(False, False, 'Kadcar_Empty', 'Metal_Sheet.001')
    rename_object_in_scene('Metal_Sheet.001', 'Metal_Sheet')
    
    deselect_all_scene_objects()
    relink_collection('headlight_panels', 'kadcar')

def add_rims_to_kadcar(rim_gltf_path):
    import_scene_into_collection(rim_gltf_path, 'rims')
    
    # car_parts_json = os.path.join(dirname, 'car_parts.json')
    # rim_object_names = extract_data_from_json(car_parts_json)['rims']
    dirname = os.path.dirname(__file__)
    rim_object_names = extract_json_attribute_data(os.path.join(dirname, 'json_config_files/car_parts.json'), 'rims')
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
    place_object(False, False, 'Kadcar_Empty', 'Rim_FR.001')
    place_object(False, False, 'Kadcar_Empty', 'Rim_FL.001')
    place_object(False, False, 'Kadcar_Empty', 'Rim_RR.001')
    place_object(False, False, 'Kadcar_Empty', 'Rim_RL.001')

    rename_object_in_scene('Rim_FR.001', 'Rim_FR')
    rename_object_in_scene('Rim_FL.001', 'Rim_FL')
    rename_object_in_scene('Rim_RR.001', 'Rim_RR')
    rename_object_in_scene('Rim_RL.001', 'Rim_RL')

    deselect_all_scene_objects()
    relink_collection('rims', 'kadcar')

def add_spoiler_to_kadcar(kadcar_specs, spoiler_gltf_path):
    dirname = os.path.dirname(__file__)
    if kadcar_specs['Kadcar'] == 'k2p':
        return

    import_scene_into_collection(spoiler_gltf_path, 'spoilers')

    spoiler_obj_name = extract_data_from_json(os.path.join(dirname, 'json_config_files/car_parts.json'))['spoiler']

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

def add_clearance_light_to_pickup(kadcar_specs, clearance_light_gltf_path):
    dirname = os.path.dirname(__file__)

    import_scene_into_collection(clearance_light_gltf_path, 'clearance_light')

    clearance_light_obj_name = extract_data_from_json(os.path.join(dirname, 'json_config_files/car_parts.json'))['clearance_light']

    deselect_all_scene_objects()
    old_names = []
    for clearance_light_name in clearance_light_obj_name:
        print(clearance_light_name)
        old_names.append(clearance_light_name)
        spoiler = bpy.data.objects[clearance_light_name]
        spoiler.select_set(True)
        bpy.data.objects.remove(spoiler, do_unlink=True)
        bpy.ops.outliner.orphans_purge()

    place_object(False, False, 'Kadcar_Empty', 'clearance_light.001')
    rename_object_in_scene('clearance_light.001', 'clearance_light')

    deselect_all_scene_objects()
    relink_collection('clearance_light', 'kadcar')

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

def format_tire_size():
    return ""

