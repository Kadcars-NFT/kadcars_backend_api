import os
from ipfs_utils import *
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from io_utils import *

dirname = os.path.dirname(__file__)
metadata_dir = os.path.join(dirname, "../metadata_json")
kadcar_dirs_root = os.path.join(dirname, "../assets/completed_nfts/")
car_folder_path = 'C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/car_files/'

def car_file_generator():
    for dir in os.listdir(kadcar_dirs_root):
        current_kc_folder = os.path.join(kadcar_dirs_root, dir)
        for kc_dir in os.listdir(current_kc_folder):
            current_bg_folder = os.path.join(current_kc_folder, kc_dir)
            for nft_dir_name in os.listdir(current_bg_folder):
                output_file_name = nft_dir_name
                nft_dir_path = os.path.join(current_bg_folder, nft_dir_name)
                
                car_file_dest_directory = os.path.join(car_folder_path, output_file_name)
                car_file_output_path = os.path.join(car_file_dest_directory, output_file_name + ".car")
                create_dir_at_path(car_file_dest_directory)
                
                glb_path = os.path.join(nft_dir_path, nft_dir_name + "_nft.glb")

                pack_and_split_CAR_file(glb_path, car_file_output_path, output_file_name)
                print(os.listdir(car_file_dest_directory))
                
                cid = ""
                for car_file in os.listdir(car_file_dest_directory):
                    car_file_path = os.path.join(car_file_dest_directory, car_file)
                    if car_file_path == car_file_output_path:
                        print("AVOIDED " + car_file_path + "\n")
                        continue
                    
                    cid = upload_asset_to_ipfs(car_file_path)
                    print(car_file_path + "   CID: " + cid + "\n")

                add_cid_to_kc_metadata(os.path.join(nft_dir_path, "/", nft_dir_name + ".json"), cid)
                if not remove_dir_at_path(car_file_dest_directory):
                    print("Error removing directory")

                print("FINISHED : " + car_file_dest_directory)

car_file_generator()