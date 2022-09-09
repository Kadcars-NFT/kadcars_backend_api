import bpy
from bpy import context
import os
import math

path_to_glb_folder = "/usr/src/app/kadcarsnft" # If you are using Windows use r"\Users\Path\To\Folder"
path_to_jpeg_folder = "/usr/src/app/kadcarsnft"

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
bpy.ops.import_scene.fbx(filepath=os.path.join(path_to_glb_folder, "balckk.fbx")) # Import .glb file to scene
bpy.context.scene.render.filepath = path_to_jpeg_folder # Set save path for images
bpy.context.scene.render.image_settings.file_format = "JPEG" # Set image file format
# bpy.ops.object.camera_add(location=(0, 2, 4), rotation=(-0.7853, 0, 0))
# bpy.ops.object.camera_add(location=(1,6,6), rotation=(0, math.pi/2, 0))
obj_camera = bpy.data.objects["Camera"]
bpy.context.scene.camera = obj_camera
bpy.context.scene.render.engine = 'CYCLES'
bpy.ops.render.render(write_still=True) # Tell Blender to render an image

deleteAllObjects()