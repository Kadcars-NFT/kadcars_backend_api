import os
from io_utils import *

dirname = os.path.dirname(__file__)
metadata_batch_dirs_root = 'K:/kadcars_metadata_batches_bc'
metadata_batch_dirs_singles = 'K:/kadcars_metadata_batches_bc/singles'

completed = ["1", "4"]

def separator():
    for dir in os.listdir(metadata_batch_dirs_root):
        if dir in completed:
            continue

        for file in os.listdir(os.path.join(metadata_batch_dirs_root, dir)):
            data = extract_data_from_json(os.path.join(metadata_batch_dirs_root, dir, file))
            final_specs = extract_data_from_json(os.path.join(dirname, "json_config_files/defaults_for_vehicle_spec.json"))

            for spec in data["specs"]:
                final_specs["vehicle_spec"] = spec["vehicle_spec"]
                export_dictionary_to_json(final_specs, os.path.join(metadata_batch_dirs_singles, "metadata_" + str(spec["vehicle_spec"]["vehicle-information"]["vin"])))

separator()