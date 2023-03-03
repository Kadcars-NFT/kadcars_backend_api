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
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweEFDNTJiZmU3Rjk2MzkzN0Q2YWQ4NWM1NENBQmYyNzllMTM0MzRlMDYiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY3NDAyNzYzMTk3NCwibmFtZSI6Im5mdF91cGxvYWQifQ.d45mS9HwTZWbAmMbdwNKkKTVPV4_kWNT2XGtSsDlncY'
    }
    response = requests.get(str("https://api.nft.storage/bafybeihtn6sk44pxizjedv7u2nqdq3ncijwmcdxgin3tcnnqh55hckvpfm"), headers=auth)
    print(response.json())

def upload_asset_to_ipfs(asset_file, format):
    headers = {
        'Content-Type': format,
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweEFDNTJiZmU3Rjk2MzkzN0Q2YWQ4NWM1NENBQmYyNzllMTM0MzRlMDYiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY3NDAyNzYzMTk3NCwibmFtZSI6Im5mdF91cGxvYWQifQ.d45mS9HwTZWbAmMbdwNKkKTVPV4_kWNT2XGtSsDlncY'
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
    except Exception as error:
        print(error)
        print("Something went wrong with request")
        exit()

def pack_and_split_CAR_file(asset_path, output_path):
    in_path = '"{fname}"'.format(fname=asset_path)
    out_path = '"{fname}"'.format(fname=output_path)
    command = "ipfs-car --pack " + str(in_path) + " --output " + str(out_path)
    
    cid = { "name": "cid" }

    #pack CAR file, capture CID
    command_output = subprocess.run(command, shell=True, capture_output=True)
    # cid["value"] = re.match(r"b'root\sCID:\s(.+?)\\n.*", str(command_output.stdout)).groups()[0]

    #split CAR file 
    os.system("carbites split " + out_path + " --size 100MB --strategy treewalk")

def iterate_over_car_files_and_upload(car_file_dest_directory, car_file_output_path):
    glb_cid = ""
    for car_file in os.listdir(car_file_dest_directory):
        car_file_path = os.path.join(car_file_dest_directory, car_file)

        if car_file_path == car_file_output_path:
            print("AVOIDED " + car_file_path + "\n")
            continue

        glb_cid = upload_asset_to_ipfs(
            car_file_path, 'application/car')
        print(car_file_path + "   CID: " + glb_cid + "\n")
    
    return glb_cid

def pin_asset_using_cid(cid):
    command = "ipfs pin add " + cid
    
    print("Pinning asset " + cid)
    command_output = subprocess.run(command, shell=True, capture_output=True)
    print(command_output)

def add_ipfs_data_to_kc_metadata(asset_file_name, ipfs_url, destination):
    kadcar_metadata = extract_data_from_json(asset_file_name)
    print(kadcar_metadata)

    if destination == 'webp':
        kadcar_metadata["webp-ipfs"] = ipfs_url
    elif destination == 'glb':
        kadcar_metadata["view-refs"]["data"] = ipfs_url

    with open(asset_file_name, 'w') as out:
        json.dump(kadcar_metadata, out)