import bpy
from kadcar_factory import *
from scene_utils import *

def shading_orchestrator(car_collection, materials_file, format='glb'):
    f = open('colorize.json')
    data = json.load(f)
    parts_to_color = data["colorize"]
    f.close()

    car_part_objects = get_objects_from_collection_by_names(car_collection, parts_to_color)
    material_collection = import_scene_into_collection(materials_file, 'materials')

    glb_file_names = []

    count = 0
    for obj in material_collection.all_objects:
        if obj.type == 'MESH':
            file_name = 'kadcar_' + obj.name + '.' + format
            print("type: "+obj.type+"   material: "+obj.material_slots[0].name )
            transfer_materials_bulk(clean=True, src=obj, target_object_names=car_part_objects)
            select_only_objects_in_collection(car_collection)
            export_scene_as_gltf(file_name)
            glb_file_names.append(file_name)
            count += 1
        if count == 3:
            break

    delete_all_objects()
    return glb_file_names

def get_principled_bsdf_for_material(material_name):
    material = bpy.data.materials[material_name]
    material.use_nodes = True
    tree = material.node_tree
    nodes = tree.nodes
    bsdf = nodes["Principled BSDF"]

    return bsdf

def transfer_materials_bulk(clean, src, target_object_names):
    for tgt in target_object_names:
        target_object = bpy.data.objects.get(tgt)
        transfer_materials(clean, src, target_object)

def transfer_materials(clean, src, tgt):
    if clean:
        tgt.data.materials.clear() # ensure the target material slots are clean
    
    for mat in src.data.materials:
        tgt.data.materials.append(mat)

def get_material_for_given_car_part(kadcar_specs, part):
    primary_color = kadcar_specs['Material']
    material = extract_json_attribute_data('color_groupings.json', primary_color)[part]
    return material