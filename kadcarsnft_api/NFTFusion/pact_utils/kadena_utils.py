import os 
import yaml
import subprocess
import sys
import requests
import hashlib
import js2py
sys.path.insert(0, '/Users/mohannadahmad/Desktop/AppDev/Kadena/kadcars_backend_api/kadcarsnft_api/NFTFusion')
from pact_utils.encoding import *
import numpy
import time
from constants import *

# adding Folder_2 to the system path
sys.path.insert(0, '/Users/mohannadahmad/Desktop/AppDev/Kadena/kadcars_backend_api/kadcarsnft_api/NFTFusion')
from io_utils import *

dirname = os.path.dirname(__file__)
path_to_transforms_folder = os.path.join(dirname, 'metadata_json')
r2r_account = "k:b9b798dd046eccd4d2c42c18445859c62c199a8d673b8c1bf7afcfca6a6a81e3"
r2r_public_key = "b9b798dd046eccd4d2c42c18445859c62c199a8d673b8c1bf7afcfca6a6a81e3"

def get_manifest_by_id(kadcar_id):
    manifest_data = pact_fetch_local("(free.universal-ledger.get-manifest \"" + kadcar_id + "\")", mainnet_network_id, mainnet_chain_id)
    return manifest_data

def get_kadcars_by_wallet(wallet_id):
    wallet_data = pact_fetch_local("(free.kadcars-nft-policy.get-cars-in-collection-by-owner \"k:2\" \"" + wallet_id + "\")", mainnet_network_id, mainnet_chain_id)
    return wallet_data

def pact_fetch_local(pact_code, network_id, chain_id):
    cmd_string = assemble_command_for_pact_api(pact_code=pact_code, chain_id=chain_id)
    hash_string = hash_command(cmd_string)

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "hash": hash_string,
        "sigs": [],
        "cmd": cmd_string
    }

    try:
        response = requests.post("https://api.chainweb.com/chainweb/0.0/mainnet01/chain/13/pact/api/v1/local", json=payload, headers=headers)
        print(response.json())

        return response.json()
    except Exception as e:
        print(e)

def hash_command(input):
    hashinput = hashlib.blake2b(input.encode("utf-8"), digest_size=32)
    hash_digest = hashinput.digest()
    hash_uint8_array = numpy.frombuffer(hash_digest, numpy.uint8)
    
    uintstr = encoding.uint8ArrayToStr(hash_uint8_array)

    # output1 = encoding.b64url.encode("_ÁÐ'Á7µüè¹ÀµáK¢öPÌô×~$")
    output = encoding.b64url.encode(uintstr)
    
    # js2py.translate_file("EncodingUtils.js", "encoding.py")

    return output

def assemble_command_for_pact_api(pact_code, chain_id):
    #TODO: change to main net, make this more dynamic
    command = {
        "meta": {
            "chainId": chain_id,
            "creationTime": time.time(),
            "gasLimit": 200000,
            "gasPrice": 1e-8,
            "sender": r2r_account,
            "ttl": 600
        },
        "networkId": "testnet04",
        "nonce": "123",
        "payload": {
            "exec": {
                "code": pact_code,
                "data": {}
            }
        },
        "signers": []
    }

    return json.dumps(command)


#Example to get kadcars belonging to specified wallet
wallet = get_kadcars_by_wallet("k:3e84c7a7a21e69e666a82f8a38f55fe79049fa6b675860681f11f514d92ae6f5")
# print(wallet)
wallet_data = wallet['result']['data']
print(wallet_data)

token_id_list = []
token_id_to_manifest_dictionary = {}

for token in wallet_data:
    token_id_list.append(token["token-id"])
    manifest = get_manifest_by_id(token["token-id"])
    token_id_to_manifest_dictionary[token["token-id"]] = manifest

#Example to fetch manifest for kadcar 
# mf = get_manifest_by_id("Kadcars#K:2:969")
# print(mf)
# print()
