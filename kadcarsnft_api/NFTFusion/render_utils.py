import bpy
from bpy.types import Light
import json

path_to_jpeg_folder = "/usr/src/app/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets"

def rotate_render(model_file):
    for object in bpy.data.objects:
        print(object)

def setRenderDevice(device, resolution_percentage, samples):
    bpy.context.scene.cycles.device = device

    for scene in bpy.data.scenes:
        scene.cucles.device = device
        scene.render.resolution_percentage = resolution_percentage
        scene.cycles.samples = samples

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

#Method to add color to specified portion of kadcar
def colorize_kadcar_and_render(part_name, colorset, material_name):
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

        #Finish render
        bpy.context.scene.render.filepath = path_to_jpeg_folder + "/" + color # Set save path for images
        bpy.context.scene.render.image_settings.file_format = "JPEG" # Set image file format
        bpy.ops.render.render(write_still=True) # Tell Blender to render an image