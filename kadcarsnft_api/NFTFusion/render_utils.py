import bpy
from bpy.types import Light

def rotate_render(model_file):
    for object in bpy.data.objects:
        print(object)


def create_area_light_object(light_metadata):
    # bpy.ops.object.light_add(
    #     type='AREA', 
    #     # radius=light_metadata['radius'], 
    #     align=light_metadata['align'],
    #     # location=light_metadata['location'], 
    #     # rotation=light_metadata['rotation'], 
    #     # scale=light_metadata['scale']
    # )
    # light_ob = bpy.context.object
    # light = light_ob.data

    light = bpy.data.lights.new(name="test-light", type='AREA')
    print(dir(light))
    light.energy = light_metadata['energy']
    light.color = light_metadata['color']
    light.shape = light_metadata['shape']

    light.diffuse = light_metadata['diffuse_factor']
    light.specular_factor = light_metadata['specular_factor']
    light.volume_factor = light_metadata['volume_factor']

    if light_metadata['shape'] == 'RECTANGLE':
        light.size = light_metadata['size']
        light.size_y = light_metadata['size_y']

    light_object = bpy.data.objects.new(name="omarscock", object_data=light)

    light_object.location = light_metadata['location']
    light_object.rotation = light_metadata['rotation']
    light_object.scale = light_metadata['scale']