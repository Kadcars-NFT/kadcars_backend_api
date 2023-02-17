import os
from io_utils import *
import requests

dirname = os.path.dirname(__file__)
metadata_batch_dirs_root = 'K:/kadcars_metadata_batches_bc'
metadata_batch_dirs_singles = 'K:/kadcars_metadata_batches_bc/singles'

completed = ["singles"]

def cid_collector():
    for dir in os.listdir(metadata_batch_dirs_root):
        if dir in completed:
            continue
        
        f = open(os.path.join(metadata_batch_dirs_singles, "cids.txt"), "a")
        
        for file in os.listdir(os.path.join(metadata_batch_dirs_root, dir)):
            data = extract_data_from_json(os.path.join(metadata_batch_dirs_root, dir, file))

            try:
                for spec in data["specs"]:
                    # f.write(spec["vehicle_spec"]["webp-ipfs"].split("//")[1])
                    url = "https://kadcarsgateway.myfilebase.com/" + spec["vehicle_spec"]["webp-ipfs"].split("//")[1]
                    requests.get(url)
                    print(url)
            except:
                print("file error")
        
        f.close()

cid_collector()