import bpy
import json

path_to_jpeg_folder = "/usr/src/app/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets"

def set_render_output_settings(render_output_path, output_format):
    bpy.context.scene.render.filepath = render_output_path # Set save path for images
    bpy.context.scene.render.image_settings.file_format = output_format # Set image file format

def set_render_device(engine, device, resolution_percentage, samples):
    bpy.data.scenes[0].render.engine = "CYCLES"

    # Set the device_type
    bpy.context.preferences.addons[
        "cycles"
    ].preferences.compute_device_type = "CUDA"
    
    # Set the device and feature set
    bpy.context.scene.cycles.device = "GPU"
    
    # get_devices() to let Blender detects GPU device
    bpy.context.preferences.addons["cycles"].preferences.get_devices()
    print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        d["use"] = 0
        if d["name"][:6] == 'NVIDIA':
            d["use"] = 1
        print(d["name"], d["use"])
#     bpy.context.scene.render.engine = engine
#     bpy.context.scene.cycles.device = device

#     for scene in bpy.data.scenes:
#         print(scene.name)
#         scene.cycles.device = device
#         scene.render.resolution_percentage = resolution_percentage
#         scene.cycles.samples = samples

def configure_render_operation_and_render():
    bpy.ops.render.render(write_still=True)