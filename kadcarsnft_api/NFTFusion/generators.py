from numpy import extract
import bpy
import os
from kadcar_factory import add_rims_to_kadcar, add_materials_to_kadcar
from scene_utils import export_scene_as_gltf, get_objects_from_collection_by_names, import_scene_into_collection
from io_utils import extract_data_from_json

def generate_kadcars_with_rims_gltfs(kadcar_gltf_file_names, rims_gltf_file_names, filepath_prefix):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    result_gltf_filenames = kadcar_gltf_file_names

    i = 0
    j = 0
    for kc_gltf in kadcar_gltf_file_names:
        for rim_gltf in rims_gltf_file_names:
            export_file_name = 'intermediary' + str(i) + str(j) + '.glb'
            kc_gltf = os.path.join(filepath_prefix, kc_gltf)
            rim_gltf = os.path.join(filepath_prefix, rim_gltf)

            add_rims_to_kadcar(kc_gltf, rim_gltf)
            export_scene_as_gltf(export_file_name)
            bpy.ops.wm.read_factory_settings(use_empty=True)
            i += 1
            j += 1
            result_gltf_filenames.append(export_file_name)

    return result_gltf_filenames

def generate_kadcars_with_shading_gltfs(kadcars_with_rims_gltf_file_names, filepath_prefix):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    result_gltf_filenames = []

    colorize_json = os.path.join(filepath_prefix, 'colorize.json')
    car_parts_to_colorize = extract_data_from_json(colorize_json)['colorize']

    for kc_gltf in kadcars_with_rims_gltf_file_names:
        kc_gltf_filepath = os.path.join(filepath_prefix, kc_gltf)
        kc_gltf_with_shading_filenames = add_materials_to_kadcar(kc_gltf_filepath, car_parts_to_colorize, kc_gltf)
        result_gltf_filenames += kc_gltf_with_shading_filenames

    return result_gltf_filenames