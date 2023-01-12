import os
from io_utils import *

dirname = os.path.dirname(__file__)
kadcar_dirs_root = 'K:/completed_nfts'
metadata_batch_dirs_root = 'K:/kadcars_metadata_batches'

def create_vehicle_spec_batch():
    count = 0
    specs = []
    for dir in os.listdir(kadcar_dirs_root):
        current_kc_folder = os.path.join(kadcar_dirs_root, dir)
        for kc_dir in os.listdir(current_kc_folder):
            current_bg_folder = os.path.join(current_kc_folder, kc_dir)
            for nft_dir_name in os.listdir(current_bg_folder):
                metadata_file_name = nft_dir_name
                metadata_file_path = os.path.join(current_bg_folder, nft_dir_name, metadata_file_name + '.json')
                metadata = extract_data_from_json(metadata_file_path)
                
                vehicle_spec = { "vehicle_spec": metadata }
                specs.append(vehicle_spec)

                count += 1
                if count % 10:
                    batch_folder_name = os.path.join(metadata_batch_dirs_root, str(count - 10) + "-" + str(count))
                    create_dir_at_path(batch_folder_name)
                    final_specs = {
                        "specs": specs
                    }
                    export_dictionary_to_json(final_specs, os.path.join(batch_folder_name, metadata_file_name))

create_vehicle_spec_batch()