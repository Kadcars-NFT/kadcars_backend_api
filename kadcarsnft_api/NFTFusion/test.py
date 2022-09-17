import bpy
from bpy import context
import os
import math

from render_utils import create_area_light_object

path_to_glb_folder = "/usr/src/app/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets" # If you are using Windows use r"\Users\Path\To\Folder"
path_to_jpeg_folder = "/usr/src/app/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets"

def deleteAllObjects():
    """
    Deletes all objects in the current scene
    """
    deleteListObjects = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'HAIR', 'POINTCLOUD', 'VOLUME', 'GPENCIL',
                         'ARMATURE', 'LATTICE', 'EMPTY', 'LIGHT', 'LIGHT_PROBE', 'CAMERA', 'SPEAKER']

    # Select all objects in the scene to be deleted:

    for o in bpy.context.scene.objects:
        for i in deleteListObjects:
            if o.type == i:
                o.select_set(False)
            else:
                o.select_set(True)
    bpy.ops.object.delete() # Deletes all selected objects in the scene

deleteAllObjects()

glb_dirList = os.listdir(path_to_glb_folder)

removeList = [".gitignore", ".DS_Store"] # If you have . files in your directory
glb_dirList = [x for x in glb_dirList if (x not in removeList)]


# bpy.ops.import_scene.gltf(filepath=os.path.join(path_to_glb_folder, "tessst.glb")) # Import .glb file to scene
bpy.ops.import_scene.gltf(filepath=os.path.join(path_to_glb_folder, "GLTF.glb")) # Import .glb file to scene
bpy.context.scene.render.filepath = path_to_jpeg_folder # Set save path for images
bpy.context.scene.render.image_settings.file_format = "JPEG" # Set image file format
# bpy.ops.object.camera_add(location=(0, 2, 4), rotation=(-0.7853, 0, 0))
# bpy.ops.object.camera_add(location=(1,6,6), rotation=(0, math.pi/2, 0))
obj_camera = bpy.data.objects["Camera"]
bpy.context.scene.camera = obj_camera
bpy.context.scene.render.engine = 'CYCLES'

obj = bpy.data.objects["Object004.001"]
obj.rotation_mode = 'XYZ'

rotate_by = 4.21875   #How many degrees to rotate the knob for every step
start_angle = 45      #What angle to start from

# bpy.ops.object.light_add(type='AREA', location=[5, 5, 5])
# light_ob = bpy.context.object
# light = light_ob.data
# light.energy = 50
# light.color = (1, 1, 1)

# bpy.ops.object.light_add(type='AREA', location=[15, 15, 15])
# light_ob = bpy.context.object
# light = light_ob.data
# light.energy = 1000
# light.color = (1, 0, 0)

metadata = {
    "align":'WORLD',
    "location": [5,5,5],
    "rotation": [0,0,0],
    "scale": [0.683125, 2.105, 0.683],
    "energy": 1000,
    "color": [0,1,0],
    "diffuse_factor": 1.0,
    "specular_factor": 1.0,
    "volume_factor": 1.0,
    "shape": 'RECTANGLE',
    "size": 0.25,
    "size_y": 0.25,
}
metadata2 = {
    "align":'WORLD',
    "location": [15,15,15],
    "rotation": [0,0,0],
    "scale": [0.683125, 2.105, 0.683],
    "energy": 1000,
    "color": [1,0,0],
    "diffuse_factor": 1.0,
    "specular_factor": 1.0,
    "volume_factor": 1.0,
    "shape": 'RECTANGLE',
    "size": 0.25,
    "size_y": 0.25,
}

create_area_light_object(metadata)
create_area_light_object(metadata2)

# for x in range(1,65):
#     angle = (start_angle * (math.pi/180)) + (x-1) * (rotate_by * (math.pi/180))
#     obj.rotation_euler = ( angle, 0,  0)

bpy.ops.render.render(write_still=True) # Tell Blender to render an image


deleteAllObjects()