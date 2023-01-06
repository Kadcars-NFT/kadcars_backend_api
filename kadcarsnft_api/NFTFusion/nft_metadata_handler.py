import os
from scene_utils import *
from shader_utils import *
from io_utils import extract_data_from_json
from stat_dictionaries import *

def build_car_metadata(kadcar_specs):
    dirname = os.path.dirname(__file__)

    if kadcar_specs['Kadcar'] == "k2p":
        clearance_light_file = "clearance_light_1"
        
        if kadcar_specs['Spoiler'] == 'spoiler_2':
            clearance_light_file = "clearance_light_2"

        kadcar_specs['Spoiler'] = clearance_light_file

    kadcar_export_file_name = str(
        kadcar_specs['Kadcar'] + "_" + kadcar_specs['Rim'] + "_" +
        kadcar_specs['Spoiler'] + "_" + kadcar_specs['Trim'] + "_" + 
        kadcar_specs['Color'] + "_" + kadcar_specs['Material'] + "_" + 
        kadcar_specs['Background']
    )

    spoiler_clearance_light_meta = None
    
    if kadcar_specs['Kadcar'] == 'k2p':
        spoiler_clearance_light_meta = ({
            "name": "clearance-light",
            "stats": [
                {
                    "key": "clearance-light-type",
                    "val": "clearance-light-" + kadcar_specs['Spoiler'].split('_')[1]
                }
            ]
        })
    else:
        spoiler_clearance_light_meta = ({
            "name": "spoiler",
            "stats": [
                {
                    "key": "spoiler-type",
                    "val": feature_names['spoilers'][kadcar_specs['Spoiler']]
                },
                {
                    "key": "handling",
                    "val": {
                        "value": kadcar_stats[kadcar_specs['Kadcar']]['spoiler']['handling'],
                        "unit": ""
                    }
                },
                {
                    "key": "downforce",
                    "val": {
                        "value": kadcar_stats[kadcar_specs['Kadcar']]['spoiler']['downforce'],
                        "unit": ""
                    }
                },
                {
                    "key": "aerodynamic-factor",
                    "val": {
                        "value": kadcar_stats[kadcar_specs['Kadcar']]['spoiler']['aerodynamic-factor'],
                        "unit": ""
                    }
                }
            ]
        })

    kadcar_metadata_json = extract_data_from_json(os.path.join(dirname, "json_config_files/kc_metadata.json"))
    kadcar_metadata_components = kadcar_metadata_json["mutable-state"]["components"]
    kadcar_metadata_components.append(spoiler_clearance_light_meta)
    
    if kadcar_specs['Kadcar'] == "k2":
        update_metadata_stat(kadcar_metadata_components, "spoiler", "spoiler-type", feature_names['spoilers'][kadcar_specs['Spoiler']])
    else:
        update_metadata_stat(kadcar_metadata_components, "clearance-light", "clearance-light-type", feature_names['spoilers'][kadcar_specs['Spoiler']])

    #Cosmetic stats
    update_metadata_stat(kadcar_metadata_components, "body", "body-type", kadcar_specs['Kadcar'])
    update_metadata_stat(kadcar_metadata_components, "wheel", "rim-type", feature_names['rims'][kadcar_specs['Rim']])
    update_metadata_stat(kadcar_metadata_components, "body", "body-material", { "type": "material", "id": kadcar_specs['Material'] + feature_names['colors'][kadcar_specs['Color']] })
    update_visual_stat_type_and_id_in_metadata(kadcar_metadata_components, kadcar_specs, 'rim', 'material', rim_materials[kadcar_specs['Rim']])

    #Performance stats
    update_metadata_stat(kadcar_metadata_components, "body", "downforce", { "value": kadcar_stats[kadcar_specs['Kadcar']]['downforce'], "unit": "%"})
    update_metadata_stat(kadcar_metadata_components, "body", "aerodynamic-factor", { "value": kadcar_stats[kadcar_specs['Kadcar']]['aerodynamic-factor'], "unit": "%"})

    #Engine stats

    
    #Derived stats


    # return kadcar_export_file_name, kadcar_metadata
    return kadcar_export_file_name, kadcar_metadata_json

def update_metadata_stat(kadcar_metadata, primary, secondary, value):
    for metadata in kadcar_metadata:
        if metadata["name"] == primary:
            for stat in metadata["stats"]:
                if stat["key"] == secondary:
                    stat["val"] = value

def update_visual_stat_type_and_id_in_metadata(kadcar_metadata_components, kadcar_specs, part, type, stat_val_id):
    for metadata in kadcar_metadata_components:
        for stat in metadata["stats"]:
            if stat["key"] == str(part + "-material"):
                stat["val"]["type"] = type
                    
                if part == 'Car_Body':
                    stat_val_id = feature_names[kadcar_specs['Color']]

                # stat["val"]["id"] = kadcar_specs['Material'] + "-" + kadcar_specs['Color']
                stat["val"]["id"] = stat_val_id

