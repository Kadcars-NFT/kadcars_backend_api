# 1. Triggered by event(contract or site)
# 2. Pull pact I'd from contract to get nfts + location
# 3. Download assets 
# 4. Import assets → blender
# 5. Build nodes to add supplementary (sticker) to car.
#     1. With Op (Location)
# 6. Add hdri
# 7. Render
# 8. Split to CAR Files
# 9. Upload CAR files + render to ipfs
# 10. Create meta data update list (from 4 above)

# 10.1 replace top uri (webp)
# 10.2 replace mutable state with new body-stickers [loc, refid]
# 10.3 replace view refs with new glb + ref to sticker nft
import bpy
from scene_utils import *
from render_utils import *
from shader_utils import *
from ipfs_utils.ipfs_utils import *
import yaml

dirname = os.path.dirname(__file__)
path_to_transforms_folder = os.path.join(dirname, 'metadata_json')
path_to_assets_folder = os.path.join(dirname, 'assets')
path_to_background_config = os.path.join(dirname, 'background_config_files')

nft = "K:/completed_nfts_2/batch_20/k2/storage/k2_rims_1_spoiler_1_steel_darkgray_glossy_storage_white_carbon_fiber/nft_2120.glb"
uv_nft = "C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/uv_gltfs/Kadcar_UV.glb"
hdri = "C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/hdr_files/storage_background.exr"
sticker = "C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/textures/wiz.png"
# nft = "C:/Users/Mohannad Ahmad/Desktop/nft_1.glb"
# uv_nft = "C:/Users/Mohannad Ahmad/Desktop/Kadcar_UV.glb"
# hdri = "C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/hdr_files/beach_background.hdr"
# sticker = "C:/Users/Mohannad Ahmad/Desktop/AppDev/Kadena/kadcars_backend/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/textures/wiz.png"

r2r_public_key = "b9b798dd046eccd4d2c42c18445859c62c199a8d673b8c1bf7afcfca6a6a81e3"

def handle_upgrade(kadcar_id, upgrade_id, upgrade_type):
    handle_upgrade_contract_trigger()

    # pact_id = extract_pact_id_from_contract_for_upgrade_details()
    # upgrade_info = get_upgrade_from_blockchain(pact_id)

    # car_nft = get_nft_from_blockchain(upgrade_info['car_nft_id'])
    # sticker_nft = get_nft_from_blockchain(upgrade_info['sticker_nft_id'])

    # car_nft_assets = download_assets(car_nft['glb'])
    # sticker_nft_assets = download_assets(sticker_nft['sticker_nft'])

    load_assets_into_blender()

    nft_glb_asset_path = apply_sticker_to_uv_maps_and_bake()

    nft_webp_asset_path = render_upgraded_nft()

    glb_url, webp_url = upload_nft_files_to_ipfs(nft_glb_asset_path, nft_webp_asset_path)
    # create_metadata_for_upgraded_nft()
    # replace_top_uri()
    # replace_mutable_state_with_upgrade_nft_data()
    # replace_view_refs_with_glb_ref_to_upgrade()


def handle_upgrade_contract_trigger():
    pass

def extract_pact_id_from_contract_for_upgrade_details():
    pass

def get_upgrade_from_blockchain(pact_id):
    #create get url
    #call get mainnet
    pass

def get_nft_from_blockchain():
    pass

def download_assets():
    pass

def load_assets_into_blender():
    #import the main car
    import_scene_into_collection(nft, 'kadcar')

    #import the UV car
    import_scene_into_collection(uv_nft, 'uv_kadcar')

def apply_sticker_to_uv_maps_and_bake():
    permanent_node_names = ["Principled BSDF", "Material Output", "BAKED_TEXTURE"]
    deselect_all_scene_objects()

    og_kadcar_body = select_object_by_name_and_make_active('Car_Body')
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

    uv_kadcar_body = select_object_by_name_and_make_active('Car_Body.001')
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

    #Link object data
    bpy.ops.object.make_links_data(type='OBDATA')

    #Fix the rotation
    bpy.context.view_layer.objects.active = og_kadcar_body
    og_kadcar_body.rotation_quaternion.x = 1.0
    apply_transform_to_selected_object(og_kadcar_body, location=True, rotation=True)

    deselect_all_scene_objects()
    delete_objects_from_collection_name('uv_kadcar')

    #Retrieve bsdf values and node tree
    bsdf = get_principled_bsdf_for_active_material(og_kadcar_body)
    kadcar_color = get_input_value_from_bsdf(bsdf, 'Base Color')
    metallic_value = get_input_value_from_bsdf(bsdf, 'Metallic')
    node_tree = get_node_tree_for_selected_object(og_kadcar_body)
    nodes = node_tree.nodes

    #Create texture shader node for sticker
    texture_node = nodes.new("ShaderNodeTexImage")
    texture_node.image = bpy.data.images.load(sticker)
    texture_node.name = "STICKER_NODE"

    #Create UV map node to specify destination
    uv_node = nodes.new("ShaderNodeUVMap")
    uv_node.uv_map = "UVMap.002" #TODO: change hard-coded uv map location
    uv_node.name = "UV_MAP_NODE"

    #Create Mix RGB node to set kadcar color
    mix_node = nodes.new("ShaderNodeMixRGB")
    mix_node.inputs['Color1'].default_value = kadcar_color
    mix_node.name = "MIX_NODE"

    #Link all created nodes to the principled bsdf
    node_tree.links.new(uv_node.outputs['UV'], texture_node.inputs['Vector'])
    node_tree.links.new(texture_node.outputs['Color'], mix_node.inputs['Color2'])
    node_tree.links.new(texture_node.outputs['Alpha'], mix_node.inputs['Fac'])
    node_tree.links.new(mix_node.outputs['Color'], bsdf.inputs['Base Color'])

    #Baking begins here
    deselect_all_scene_objects()
    
    #Set up baking parameters
    bsdf.inputs['Metallic'].default_value = 0.0
    configure_bake_settings('CYCLES', 'CUDA', 'GPU', False, False, False, 'DIFFUSE')
    
    #Select the main uv map for the kadcar
    uv_layers = og_kadcar_body.data.uv_layers
    uv_layer_names = [uv.name for uv in uv_layers]
    for name in uv_layer_names:
        if name == "UVMap":
            uv_layers[name].active = True
            print(name)
            print(uv_layers[name])

    #Create a new texture image shader node for the baked texture destination
    image_name = "baked_texture_image"
    image = bpy.data.images.new(image_name, 4096, 4096)
    bake_texture_node = nodes.new("ShaderNodeTexImage")
    bake_texture_node.select = True
    bake_texture_node.name = "BAKED_TEXTURE"
    nodes.active = bake_texture_node
    bake_texture_node.image = image
    
    #Select the kadcar body and bake
    select_object_by_name_and_make_active('Car_Body')
    bpy.ops.object.bake('INVOKE_DEFAULT', type='DIFFUSE', pass_filter={'COLOR'}, save_mode='EXTERNAL', target='IMAGE_TEXTURES')

    #Remove old unneeded nodes
    for node in nodes:
        print(node.name)
        if node.name not in permanent_node_names:
            nodes.remove(node)
    
    #Link new baked texture shader node to the principled bsdf
    node_tree.links.new(bake_texture_node.outputs['Color'], bsdf.inputs['Base Color'])
    
    #Restore the metallic value of the car 
    set_input_value_in_bsdf(bsdf, 'Metallic', metallic_value)

    #Complete scene details and export
    glb_path = 'K:/test_uv.glb'
    add_hdri_to_scene('storage')
    export_scene_as_gltf(glb_path)

    return glb_path

def add_hdri_to_scene(background_name):
    hdr_file_path = os.path.join(path_to_assets_folder, "hdr_files/" + background_name + "_background")

    if background_name == 'storage':
        hdr_file_path = hdr_file_path + ".exr"
    else:
        hdr_file_path = hdr_file_path + ".hdr"

    customize_world_shader_nodes(hdr_file_path, background_name)

def render_upgraded_nft():
    render_path = 'K:/test_uv'
    bg_config_data = extract_json_attribute_data(os.path.join(path_to_background_config, "backgrounds_config.json"), 'storage') #TODO: change hard-coded bg name
    
    configure_render_settings('CYCLES', 'CUDA', 'GPU', 200, 50)
    set_render_output_settings(render_path, 'WEBP', bg_config_data['render_settings']['res_x'], bg_config_data['render_settings']['res_y'], True)

    return render_path + '.webp'

def upload_nft_files_to_ipfs(nft_asset_path, render_asset_path):
    destination = nft_asset_path.split('/')[len(nft_asset_path.split('/')) - 1] + ".car"
    
    car_file_dest_directory = 'K:/car_file/'
    car_file_dest_file = os.path.join(car_file_dest_directory, destination)

    pack_and_split_CAR_file(nft_asset_path, car_file_dest_file)
    glb_cid = iterate_over_car_files_and_upload(car_file_dest_directory, car_file_dest_file)
    glb_url = "ipfs://" + glb_cid

    webp_cid = upload_asset_to_ipfs(render_asset_path, 'image/*')
    webp_url = "ipfs://" + webp_cid

    return glb_url, webp_url

def create_metadata_for_upgraded_nft():
    pass

def replace_top_uri(webp_ipfs_url):
    transform_data = extract_data_from_json(os.path.join(path_to_transforms_folder, 'transforms.json'))

    transform_data[2]["transform"]["obj"]["uri"]["data"] = webp_ipfs_url

def replace_mutable_state_with_upgrade_nft_data():
    pass

def replace_view_refs_with_glb_ref_to_upgrade(glb_ipfs_url):
    transform_data = extract_data_from_json(os.path.join(path_to_transforms_folder, 'transforms.json'))

    transform_data[0]["transform"]["obj"]["new-datum"]["datum"]["art-asset"]["data"] = glb_ipfs_url

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
# handle_upgrade()