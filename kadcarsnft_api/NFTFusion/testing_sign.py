import os 
import yaml
import subprocess
from io_utils import *

dirname = os.path.dirname(__file__)
path_to_transforms_folder = os.path.join(dirname, 'metadata_json')
r2r_public_key = "b9b798dd046eccd4d2c42c18445859c62c199a8d673b8c1bf7afcfca6a6a81e3"

def sign_using_pact_cli(transforms):
    data = {
        "pactTxHash": "",
        "step": 0,
        "rollback": False,
        "data": transform_data,
        "networkId": "testnet04",
        "publicMeta": [
            {"chainId": "1"}, 
            {"sender": r2r_public_key}, 
            {"gasLimit": 150000}, 
            {"gasPrice": 0.00000001}, 
            {"ttl": 600}
        ],
        "type": "cont"
    }

    #prepare unsigned transaction data
    path_to_tx_yaml = os.path.join(path_to_transforms_folder, "tx.yaml")
    path_to_r2r_key_yaml = os.path.join(path_to_transforms_folder, "keyset.yaml")
    path_to_tx_final_yaml = os.path.join(path_to_transforms_folder, "tx-final.yaml")
    path_to_tx_signed_yaml = os.path.join(path_to_transforms_folder, "tx-signed.yaml")
    path_to_tx_unsigned_yaml = os.path.join(path_to_transforms_folder, "tx-unsigned.yaml")



    #create tx file with above data
    with open(path_to_tx_yaml, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        
    #Convert the transaction to an unsigned prepared form that signatures can be added to
    subprocess.run("pact -u " + path_to_tx_yaml + " > " + path_to_tx_unsigned_yaml)
    
    #sign the prepared transaction
    subprocess.run("cat " + path_to_tx_unsigned_yaml + " | " + "pact add-sig " + path_to_r2r_key_yaml + " > " + path_to_tx_signed_yaml)

    #combine the signatures into transaction ready to be sent to blockchain
    subprocess.run("pact combine-sigs " + path_to_tx_signed_yaml + " > " + path_to_tx_final_yaml)

transform_data = extract_data_from_json(os.path.join(path_to_transforms_folder, 'transforms.json'))

sign_using_pact_cli(transform_data[0])