import os
from io_utils import *

dirname = os.path.dirname(__file__)
kadcar_dirs_root = 'D:/completed_nfts'
metadata_batch_dirs_root = 'D:/kadcars_metadata_batches_bc'


def create_vehicle_spec_batch():
    count = 3701

    # count = 1
    specs = []
    batch_folder_name = ""
    single = False

    print("Is this a single? Press y for yes")
    answer = input()
    if answer == 'y':
        single = True

    for dir in os.listdir(kadcar_dirs_root):
        current_batch_folder = os.path.join(kadcar_dirs_root, dir)

        if os.path.isdir(current_batch_folder) == False:
            continue
        # print(current_batch_folder)
        for batch_dir in os.listdir(current_batch_folder):
            current_kc_folder = os.path.join(current_batch_folder, batch_dir)
            if os.path.isdir(current_kc_folder) == False:
                continue
            # print(current_kc_folder)
            for kc_dir in os.listdir(current_kc_folder):
                current_bg_folder = os.path.join(current_kc_folder, kc_dir)
                if os.path.isdir(current_bg_folder) == False:
                    continue
                for nft_dir_name in os.listdir(current_bg_folder):
                    current_nft_path = os.path.join(current_bg_folder, nft_dir_name)
                    if os.path.isdir(current_nft_path) == False:
                        continue
                    # print(current_nft_path)
                    for file in os.listdir(current_nft_path):
                        if 'metadata' not in file:
                            continue
                        
                        metadata_file_name = file
                        metadata_file_path = os.path.join(current_bg_folder, nft_dir_name, metadata_file_name)
                        metadata = extract_data_from_json(metadata_file_path)
                        final_specs = extract_data_from_json(os.path.join(dirname, "json_config_files/defaults_for_vehicle_spec.json"))
                        
                        metadata['mutable-state']['components'][4]['stats'].append({
                            "key": "horsepower",
                            "val": {
                                "value": 754.0,
                                "unit": "hp"
                            }
                        })
                        metadata['mutable-state']['components'][4]['stats'].append({
                            "key": "braking-power",
                            "val": {
                                "value": 70.0,
                                "unit": "%"
                            }
                        })
                        # metadata['vehicle-information']['vin'] = metadata_file_name.split('_')[1].split('.')[0]
                        metadata['vehicle-information']['vin'] = count
                        
                        vehicle_spec = { "vehicle_spec": metadata }
                        specs.append(vehicle_spec)

                        final_specs["specs"] = specs

                        if count % 2 == 0:
                            specs = []
                            name = metadata_file_name.split('.')[0].split('_')[0] + "_" + str(count)
                            export_dictionary_to_json(final_specs, os.path.join(metadata_batch_dirs_root, name))
                        
                        count += 1

create_vehicle_spec_batch()