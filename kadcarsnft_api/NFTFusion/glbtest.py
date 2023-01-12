from pygltflib import GLTF2
import os

dirname = os.path.dirname(__file__)

filepath = 'C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/completed_nfts/k2/beach/k2_rims_5_spoiler_1_carbon_fiber_cyan_steel_beach'

gltf = GLTF2()
gltf = gltf.load(os.path.join(filepath, "nft.glb"))
print(gltf.extras)