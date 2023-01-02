import os
import re
import json
import requests
import subprocess
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from io_utils import *

IPFS_URL_PREFIX = "https://api.nft.storage/"

def get_asset_from_ipfs(cid):
    auth = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweENmOTAyMjk0MDE3NUE3ZmM5MUJiMDM0NDE3ZjQ1MDhkRjBEOWMyNjMiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY2ODI5OTcyODMzNCwibmFtZSI6ImtleXMifQ.jP_EGo6JSyf6bt9xxJld1TGjgb_fV7ES9yXX84wr2I4'
    }
    response = requests.get(str("https://api.nft.storage/bafybeihtn6sk44pxizjedv7u2nqdq3ncijwmcdxgin3tcnnqh55hckvpfm"), headers=auth)
    print(response.json())

def upload_asset_to_ipfs(asset_file, format):
    headers = {
        'Content-Type': format,
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweENmOTAyMjk0MDE3NUE3ZmM5MUJiMDM0NDE3ZjQ1MDhkRjBEOWMyNjMiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY2ODI5OTcyODMzNCwibmFtZSI6ImtleXMifQ.jP_EGo6JSyf6bt9xxJld1TGjgb_fV7ES9yXX84wr2I4'
    }
    
    response = None
    try:
        # with open(asset_file, 'rb') as f:
        #     response = requests.post(IPFS_URL_PREFIX + 'upload/', headers=headers, files={asset_file: f})
            
        response = requests.post(url=IPFS_URL_PREFIX + "upload/", data=open(asset_file, 'rb'), headers=headers)
        print(response.json())
        if response.ok == True:
            cid = response.json()["value"]["cid"]
            return cid
    except:
        print("Something went wrong with request")

def pack_and_split_CAR_file(asset_path, output_path, asset_file_name):
    in_path = '"{fname}"'.format(fname=asset_path)
    out_path = '"{fname}"'.format(fname=output_path)
    command = "ipfs-car --pack " + str(in_path) + " --output " + str(out_path)
    
    cid = { "name": "cid" }

    #pack CAR file, capture CID
    command_output = subprocess.run(command, shell=True, capture_output=True)
    # cid["value"] = re.match(r"b'root\sCID:\s(.+?)\\n.*", str(command_output.stdout)).groups()[0]

    #split CAR file 
    os.system("carbites split " + out_path + " --size 100MB --strategy treewalk")

def add_ipfs_data_to_kc_metadata(asset_file_name, cid, keys_array):
    kadcar_metadata = extract_data_from_json(asset_file_name)
    
    if kadcar_metadata:
        kadcar_metadata["cid"] = cid
        export_dictionary_to_json(kadcar_metadata, asset_file_name)