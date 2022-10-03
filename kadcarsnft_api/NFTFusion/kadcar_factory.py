import bpy
import json
from scene_utils import delete_all_objects, export_scene_as_gltf, get_objects_from_collection_by_names, select_only_objects_in_collection
from shader_utils import transfer_materials_bulk
from shader_utils import transfer_materials
from scene_utils import deselect_all_scene_objects, import_scene_into_collection

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

def add_rims_to_kadcar(rim_type, rim_file, color):
    if rim_type == 1:
        bpy.ops.import_scene.gltf(filepath=rim_file) # Import .glb file to scene
        replace_object(should_transfer_w_materials=True, should_clear_old_materials=True, source_name='wheel_10_Plane_007.002', target_name='wheel_3_Cylinder_021.004')
        replace_object(should_transfer_w_materials=True, should_clear_old_materials=True, source_name='wheel_10_Plane_007.001', target_name='wheel_3_Cylinder_021.005')

#TODO: rename replaced object
def replace_object(should_transfer_w_materials, should_clear_old_materials, source_name, target_name):
    source_object = bpy.data.objects.get(source_name)
    target_object = bpy.data.objects.get(target_name)

    target_object.location.x = source_object.location.x
    target_object.location.y = source_object.location.y
    target_object.location.z = source_object.location.z

    target_object.rotation_quaternion.w = source_object.rotation_quaternion.w
    target_object.rotation_quaternion.x = source_object.rotation_quaternion.x
    target_object.rotation_quaternion.y = source_object.rotation_quaternion.y
    target_object.rotation_quaternion.z = source_object.rotation_quaternion.z

    if should_transfer_w_materials:
        transfer_materials(should_clear_old_materials, source_object, target_object)
    
    deselect_all_scene_objects()
    source_object.select_set(True)
    bpy.ops.object.delete()

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
            transfer_materials_bulk(clean=True, src=obj, target_list=car_part_objects)
            select_only_objects_in_collection(car_collection)
            export_scene_as_gltf(file_name)
            glb_file_names.append(file_name)

    delete_all_objects()
    return glb_file_names