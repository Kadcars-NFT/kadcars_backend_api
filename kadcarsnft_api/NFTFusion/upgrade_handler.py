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
from scene_utils import import_scene_into_collection, deselect_all_scene_objects, customize_world_shader_nodes
from render_utils import *
from shader_utils import get_principled_bsdf_for_active_material

nft = "K:\completed_nfts_2/batch_20\k2\storage\k2_rims_1_spoiler_1_steel_darkgray_glossy_storage_white_carbon_fiber/nft_59.glb"
uv_nft = "K:\\completed_nfts\\batch_0\\k2\\beach\\k2_rims_1_spoiler_1_carbon_fiber_black_metallic_beach_white_grated\\nft_0.glb"
sticker = "C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/textures/wiz.png"
hdri = "C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/hdr_files\storage_background.exr"

def handle_upgrade():
    handle_upgrade_contract_trigger()

    # pact_id = extract_pact_id_from_contract_for_upgrade_details()
    # upgrade_info = get_upgrade_from_blockchain(pact_id)

    # car_nft = get_nft_from_blockchain(upgrade_info['car_nft_id'])
    # sticker_nft = get_nft_from_blockchain(upgrade_info['sticker_nft_id'])

    # car_nft_assets = download_assets(car_nft['glb'])
    # sticker_nft_assets = download_assets(sticker_nft['sticker_nft'])

    load_assets_into_blender()
    copy_uv_maps_from_source()

    # build_shader_nodes_for_sticker_upgrade()
    # add_hdri_to_scene()
    # render_upgraded_nft()
    # split_nft_to_car_files()
    # upload_car_file()
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
    import_scene_into_collection(nft, 'kadcar')

# def copy_uv_maps_from_source(source_car):
#     deselect_all_scene_objects()
#     import_scene_into_collection(uv_nft, 'uv_nft')
#     context = bpy.context
#     obj = context.active_object
#     uv_layer_names = [uv.name for uv in obj.data.uv_layers]

#     if uv_layer_names:
#         for ob in context.selected_objects:
#             if ob != obj and ob.type =='MESH':
#                 for uv_map in uv_layer_names:
#                     obj.data.uv_layers[uv_map].active = True
#                     if uv_map not in ob.data.uv_layers:
#                         ob.data.uv_layers.new(name=uv_map)
#                     ob.data.uv_layers[uv_map].active = True
#                     bpy.ops.object.join_uvs()

def copy_uv_maps_from_source(source_car):
    #1. make metallic value 0
    deselect_all_scene_objects()

    kadcar_empty = bpy.data.objects.get('Car_Body')
    kadcar_empty.select_set(True)

    bpy.context.view_layer.objects.active = kadcar_empty
    bsdf = get_principled_bsdf_for_active_material(kadcar_empty)
    bsdf.inputs['Metallic'].default_value = 0.0

    # 2. get the UV map
    uv_layers = kadcar_empty.data.uv_layers
    door_uv = None
    hood_uv = None

    for uv in uv_layers:
        if uv.name == "UV_Hood":
            hood_uv = uv
        if uv.name == "UV_Door":
            door_uv = uv
        
        

    print(uv_layers)

def build_shader_nodes_for_sticker_upgrade(location):
    pass

def add_hdri_to_scene():
    customize_world_shader_nodes(hdri, 'storage')

def render_upgraded_nft():
    configure_render_settings('CYCLES', 'CUDA', 'GPU', 200, 50)
    set_render_output_settings("K:/UpgradeTest/render", 'WEBP', 1920, 1192, True)

def split_nft_to_car_files():
    pass

def upload_car_file():
    pass

def create_metadata_for_upgraded_nft():
    pass

def replace_top_uri():
    pass

def replace_mutable_state_with_upgrade_nft_data():
    pass

def replace_view_refs_with_glb_ref_to_upgrade():
    pass

handle_upgrade()