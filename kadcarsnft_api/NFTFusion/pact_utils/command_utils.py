import os 
import yaml
import subprocess
import sys
import requests
import hashlib
import js2py
from encoding import *
import numpy
import time

# adding Folder_2 to the system path
sys.path.insert(0, '/Users/mohannadahmad/Desktop/AppDev/Kadena/kadcars_backend_api/kadcarsnft_api/NFTFusion')
from io_utils import *

dirname = os.path.dirname(__file__)
path_to_transforms_folder = os.path.join(dirname, 'metadata_json')
r2r_account = "k:b9b798dd046eccd4d2c42c18445859c62c199a8d673b8c1bf7afcfca6a6a81e3"
r2r_public_key = "b9b798dd046eccd4d2c42c18445859c62c199a8d673b8c1bf7afcfca6a6a81e3"

def sign_using_pact_cli(transforms, pact_id):
    print(transforms)
    data = {
        "pactTxHash": pact_id,
        "step": 1,
        "rollback": False,
        "data": transforms,
        "networkId": "testnet04",
        "signers": [{"public":r2r_public_key}],
        "publicMeta": {
            "chainId": "1", 
            "sender": r2r_account, 
            "gasLimit": 150000, 
            "gasPrice": 0.00000001, 
            "ttl": 600
        },
        "type": "cont"
    }

    #prepare unsigned transaction data
    path_to_tx_yaml = "tx.yaml"
    path_to_r2r_key_yaml = "keyset.yaml"
    path_to_tx_signed_yaml = "tx-signed.yaml"
    path_to_tx_unsigned_yaml = "tx-unsigned.yaml"

    #create tx file with above data
    with open(path_to_tx_yaml, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    #Convert the transaction to an unsigned prepared form that signatures can be added to
    subprocess.run("pact -u " + path_to_tx_yaml + " > " + path_to_tx_unsigned_yaml, shell=True)
    
    #sign the prepared transaction
    subprocess.run("cat " + path_to_tx_unsigned_yaml + " | " + "pact add-sig " + path_to_r2r_key_yaml + " > " + path_to_tx_signed_yaml, shell=True)

def send_transaction():
    command = ""
    
    with open("tx-signed.yaml", 'r') as f:
        command = f.read()
    f.close()

    print(command)

    headers = {
        "Content-Type": "application/json"
    }
    command = json.loads(command,)
    print(command)
    response = requests.post("https://api.testnet.chainweb.com/chainweb/0.0/testnet04/chain/1/pact/api/v1/send", headers=headers, json=command)
    print(response.text)


def hash_command(input):
    hashinput = hashlib.blake2b(input.encode("utf-8"), digest_size=32)
    hash_digest = hashinput.digest()
    hash_uint8_array = numpy.frombuffer(hash_digest, numpy.uint8)
    
    uintstr = encoding.uint8ArrayToStr(hash_uint8_array)

    output = encoding.b64url.encode("_ÁÐ'Á7µüè¹ÀµáK¢öPÌô×~$")
    output1 = encoding.b64url.encode(uintstr)
    
    # js2py.translate_file("EncodingUtils.js", "encoding.py")
    print(uintstr)
    print("HARDCODED")
    print(output)
    print("NEW")
    print(output1)

    return output

def assemble_command_for_pact_api(pact_code):
    #TODO: change to main net, make this more dynamic
    command = {
        "meta": {
            "chainId": "1",
            "creationTime": time.time(),
            "gasLimit": 150000,
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

input = "{\"networkId\":\"testnet04\",\"payload\":{\"cont\":{\"proof\":null,\"data\":{\"kc\":{\"pred\":\"keys-all\",\"keys\":[\"f157854c15e9bb8fb55aafdecc1ce27a3d60973cbe6870045f4415dc06be06f5\"]},\"transformation-list\":[{\"transform\":{\"obj\":{\"uri\":{\"data\":\"view-references\",\"scheme\":\"ipfs\"},\"new-datum\":{\"hash\":\"6Te22fUzf-9ynFfzYTYnKLzVVU2JhqhimJPgYGyuAwQ\",\"uri\":{\"data\":\"view-references\",\"scheme\":\"pact:schema\"},\"datum\":{\"art-asset\":{\"data\":\"ipfs://bafybeielzyapofnglxicaith7etxczpxq3psaeq6uh7chuh6dtbbmtqyny\",\"scheme\":\"ipfs://\"}}}},\"type\":\"replace\"}},{\"transform\":{\"obj\":{\"hash\":\"6Te22fUzf-9ynFfzYTYnKLzVVU2JhqhimJPgYGyuAwQ\",\"uri\":{\"data\":\"nft-references\",\"scheme\":\"pact:schema\"},\"datum\":{\"test\":\"test\"}},\"type\":\"add\"}},{\"transform\":{\"obj\":{\"uri\":{\"data\":\"ipfs://bafybeia3obqfvgnxpm56oan2b7mempewuml4xynlcgkodks6tf44b3hnie\",\"scheme\":\"ipfs\"}},\"type\":\"uri\"}}]},\"pactId\":\"DycORcKohpEWlyC6VxX9pcT28y_bP-G52xjlGqAaUVc\",\"rollback\":false,\"step\":2}},\"signers\":[{\"pubKey\":\"b9b798dd046eccd4d2c42c18445859c62c199a8d673b8c1bf7afcfca6a6a81e3\"}],\"meta\":{\"creationTime\":1678004406,\"ttl\":6000,\"gasLimit\":150000,\"chainId\":\"1\",\"gasPrice\":1.0e-8,\"sender\":\"k:b9b798dd046eccd4d2c42c18445859c62c199a8d673b8c1bf7afcfca6a6a81e3\"},\"nonce\":\"\\\"2023-03-05 08:20:06.599883 UTC\\\"\"}"
output = hash_command(input)