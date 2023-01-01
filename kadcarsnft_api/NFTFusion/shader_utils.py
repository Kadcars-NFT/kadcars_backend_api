import bpy
from kadcar_factory import *
from scene_utils import *
from io_utils import *

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

def change_object_base_color(color, mtl_name, tgt_object):
    tgt_object.data.materials.clear()
    material = bpy.data.materials.new(name=mtl_name)
    bsdf = get_principled_bsdf_for_material(mtl_name)

    bsdf.inputs['Base Color'].default_value = color
    material.diffuse_color = color

    tgt_object.data.materials.append(material)

def change_object_emission_level(tgt_object):
    pass

def apply_texture_image_to_object(clean, tex_image_path, tgt_object):
    if clean:
        tgt_object.data.materials.clear()

    material = bpy.data.materials.new(name='trim_texture')
    bsdf = get_principled_bsdf_for_material('trim_texture')

    texImage = material.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load(tex_image_path)

    material.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

    if tgt_object.data.materials:
        tgt_object.data.materials[0] = material
    else:
        tgt_object.data.materials.append(material)

def transfer_materials_bulk(clean, src, target_object_names):
    print(target_object_names)
    for tgt in target_object_names:
        target_object = bpy.data.objects.get(tgt)
        transfer_materials(clean, src, target_object)

def transfer_materials(clean, src, tgt):
    if clean:
        tgt.data.materials.clear() # ensure the target material slots are clean
    
    for mat in src.data.materials:
        tgt.data.materials.append(mat)

def get_material_for_given_car_part(kadcar_specs, part):
    dirname = os.path.dirname(__file__)
    primary_color = kadcar_specs['Color']
    material = extract_json_attribute_data(os.path.join(dirname, 'json_config_files/color_groupings.json'), primary_color)[part]
    return material

def add_background_shader_node(tree_nodes, strength):
    node_background = tree_nodes.new(type='ShaderNodeBackground')
    node_background.inputs['Strength'].default_value = strength

def add_sky_texture_shader_node(tree_nodes, sky_type, sun_disc, sun_elevation, sun_rotation, air_density, dust_density, ozone_density):
    sky_texture = tree_nodes.new('ShaderNodeTexSky')

    sky_texture.sky_type = sky_type
    sky_texture.sun_disc = sun_disc
    sky_texture.sun_elevation = sun_elevation
    sky_texture.sun_rotation = sun_rotation
    sky_texture.air_density = air_density
    sky_texture.dust_density = dust_density
    sky_texture.ozone_density = ozone_density

def add_mapping_shader_node(tree_nodes, vector_type, rotation):
    mapping_node = tree_nodes.new('ShaderNodeMapping')

    mapping_node.vector_type = vector_type
    mapping_node.inputs["Rotation"].default_value = rotation

def add_texture_coordinates_shader_node(tree_nodes, from_instancer):
    tex_coord_node = tree_nodes.new('ShaderNodeTexCoord')

    tex_coord_node.from_instancer = from_instancer