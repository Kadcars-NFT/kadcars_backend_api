import bpy
import json

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

def add_rims_to_kadcar(rim_type, color):
    pass

def apply_color_to_windshield(color):
    pass

def customize_kadcar_hood(material_name):
    pass

def apply_decal_to_kadcar(decal):
    pass