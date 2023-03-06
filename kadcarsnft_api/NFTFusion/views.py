import bpy
import os
import django
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from NFTFusion.constants import *
from NFTFusion.blender_utils import deleteAllObjects
from NFTFusion.render_factory import *
from NFTFusion.upgrade_handler import handle_upgrade
from NFTFusion.io_utils import *
# Create your views here.


def renderModel(payload):
    deleteAllObjects()

    glb_dirList = os.listdir(path_to_glb_folder)

    # If you have . files in your directory
    removeList = [".gitignore", ".DS_Store"]
    glb_dirList = [x for x in glb_dirList if (x not in removeList)]

    # import the scene with in the appropriate format as indicated by the payload
    if payload["type"] == "fbx":
        bpy.ops.import_scene.fbx(filepath=os.path.join(path_to_glb_folder, "./assets/balckk.fbx"))
    elif payload["type"] == "gltf":
        bpy.ops.import_scene.fbx(filepath=os.path.join(path_to_glb_folder, "./assets/balckk.fbx"))

    # bpy.ops.import_scene.gltf(filepath=os.path.join(path_to_glb_folder, "tessst.glb")) # Import .glb file to scene
    bpy.ops.import_scene.gltf(filepath=os.path.join(
        path_to_glb_folder, "./assets/9-22.glb"))  # Import .glb file to scene
    bpy.context.scene.render.filepath = path_to_jpeg_folder  # Set save path for images
    bpy.context.scene.render.image_settings.file_format = "JPEG"  # Set image file format
    # bpy.ops.object.camera_add(location=(0, 2, 4), rotation=(-0.7853, 0, 0))
    # bpy.ops.object.camera_add(location=(1,6,6), rotation=(0, math.pi/2, 0))
    obj_camera = bpy.data.objects["Camera"]
    bpy.context.scene.camera = obj_camera
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.ops.render.render(write_still=True)  # Tell Blender to render an image

    deleteAllObjects()

@api_view(['GET'])
def testing(request):
    print("LOL")
    return HttpResponse("LOL")

@api_view(['POST'])
def apply_upgrade(request):
    dirname = os.path.dirname(__file__)

    kadcar_id = request.data['kadcar_id']
    upgrade_id = request.data['upgrade_id']
    upgrade_type = request.data['upgrade_type']

    # handle_upgrade(kadcar_id, upgrade_id, upgrade_type)
    transforms_data = extract_data_from_json(os.path.join(dirname, "metadata_json/transforms.json"))
    json_data_dump = json.dumps(transforms_data)

    return HttpResponse(json_data_dump, content_type='application/json')