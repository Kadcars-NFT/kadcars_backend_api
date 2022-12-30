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

def add_materials_and_colorize_kadcar(filepath_prefix, kadcar_specs, kadcar_metadata):
    #Add material spheres to scene
    dirname = os.path.dirname(__file__)
    material_list = ["matte", "steel", "chrome", "metallic", "glossy"]
    material_file = os.path.join(filepath_prefix, 'material_gltfs/material_spheres_new.glb')
    import_scene_into_collection(material_file, 'materials')

    colorize_data = extract_data_from_json(os.path.join(dirname, 'json_config_files/colorize.json'))
    primary_color_independent = colorize_data["independent"]
    primary_color_dependent = colorize_data["dependent"]

    kadcar_body = primary_color_independent[str('colorize-' + kadcar_specs['Kadcar'])]
    add_material_and_colorize_components(filepath_prefix, kadcar_body, str(kadcar_specs['Material'] + "-" + kadcar_specs['Color']))

    # headlights = primary_color_independent["headlights"]
    # if kadcar_specs['Kadcar'] == "k2":
    #     if kadcar_specs['Spoiler'] == "spoiler_2":
    #         add_material_and_colorize_components(filepath_prefix, headlights, str(kadcar_specs['Material'] + "_" + kadcar_specs['Color']))

    # trim = primary_color_independent["trim"]
    # update_visual_stat_in_metadata(kadcar_metadata, kadcar_specs, "trim", primary_color_independent)

    #Get materials for dependent groups
    for part in primary_color_dependent:
        components_to_colorize = primary_color_dependent[part]["objects"]
        material_name = get_material_for_given_car_part(kadcar_specs, part)

        update_visual_stat_in_metadata(kadcar_metadata["stats"]["components"], kadcar_specs, part, primary_color_dependent)

        if material_name == "default":
            continue
        add_material_and_colorize_components(filepath_prefix, components_to_colorize, material_name)
    
    return kadcar_metadata

def add_material_and_colorize_components(filepath_prefix, car_part_objects, material_name):
    material = bpy.data.objects[material_name]

    transfer_materials_bulk(clean=True, src=material, target_object_names=car_part_objects)

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
    rename_object_in_scene('Rim_RR.001', 'Rim_BR')
    rename_object_in_scene('Rim_RL.001', 'Rim_BL')

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
    for spoiler_name in clearance_light_obj_name:
        print(spoiler_name)
        old_names.append(spoiler_name)
        spoiler = bpy.data.objects[spoiler_name]
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

def build_car_metadata(kadcar_specs):
    dirname = os.path.dirname(__file__)
    component_list = ["body", "rim", "engine", "spoiler"]
    kadcar_export_file_name = str(
        kadcar_specs['Kadcar'] + "_" + kadcar_specs['Rim'] + "_" +
        kadcar_specs['Spoiler'] + "_" + kadcar_specs['Trim'] + "_" + 
        kadcar_specs['Color'] + "_" + kadcar_specs['Material'] + "_" + 
        kadcar_specs['Background']
    )

    spoiler_clearance_light_meta = None
    
    if kadcar_specs['Kadcar'] == 'k2p':
        spoiler_clearance_light_meta = ({
            "name": "clearance-light",
            "stats": [
                {
                    "key": "clearance-light-type",
                    "val": "clearance-light-" + kadcar_specs['Spoiler'].split('_')[1]
                }
            ]
        })
    else:
        spoiler_clearance_light_meta = ({
            "name": "spoiler",
            "stats": [
                {
                    "key": "spoiler-type",
                    "val": kadcar_specs['Spoiler']
                },
                {
                    "key": "handling",
                    "val": {
                        "value": "",
                        "unit": ""
                    }
                },
                {
                    "key": "downforce",
                    "val": {
                        "value": "",
                        "unit": ""
                    }
                },
                {
                    "key": "aerodynamic-factor",
                    "val": {
                        "value": "",
                        "unit": ""
                    }
                }
            ]
        })

    kadcar_metadata_json = extract_data_from_json(os.path.join(dirname, "json_config_files/kc_metadata.json"))
    kadcar_metadata_components = kadcar_metadata_json["stats"]["components"]

    kadcar_metadata_components.append(spoiler_clearance_light_meta)
    if kadcar_specs['Kadcar'] == "k2":
        # spoiler_meta[0]["stats"][0]["val"] = kadcar_specs['Spoiler']
        update_metadata_stat(kadcar_metadata_components, "spoiler", "spoiler-type", kadcar_specs['Spoiler'])
        print(spoiler_clearance_light_meta)
    else:
        update_metadata_stat(kadcar_metadata_components, "clearance-light", "clearance-light-type", kadcar_specs['Spoiler'])


    update_metadata_stat(kadcar_metadata_components, "body", "body-type", kadcar_specs['Kadcar'])
    update_metadata_stat(kadcar_metadata_components, "wheel", "rim-type", kadcar_specs['Rim'])
    update_metadata_stat(kadcar_metadata_components, "body", "body-material", { "type": "material", "id": kadcar_specs['Material'] + "-" + kadcar_specs['Color'] })
    update_metadata_stat(kadcar_metadata_components, "trim", "trim-material", { "type": "material", "id": kadcar_specs['Trim'] })

    # return kadcar_export_file_name, kadcar_metadata
    return kadcar_export_file_name, kadcar_metadata_json

def update_metadata_stat(kadcar_metadata, primary, secondary, value):
    for metadata in kadcar_metadata:
        if metadata["name"] == primary:
            for stat in metadata["stats"]:
                if stat["key"] == secondary:
                    stat["val"] = value

def update_visual_stat_in_metadata(kadcar_metadata_components, kadcar_specs, part, source_dict):
    material_list = ["matte", "steel", "chrome", "metallic", "glossy"]

    for metadata in kadcar_metadata_components:
        if metadata["name"] == source_dict[part]["component"]:
            for stat in metadata["stats"]:
                if stat["key"] == str(part + "-material"):
                    if kadcar_specs['Material'] in material_list:
                        stat["val"]["type"] = "material"
                        stat["val"]["id"] = kadcar_specs['Material'] + "-" + kadcar_specs['Color']