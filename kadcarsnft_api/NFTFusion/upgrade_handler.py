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

nft = "K:/completed_nfts_2/batch_20/k2/storage/k2_rims_1_spoiler_1_steel_darkgray_glossy_storage_white_carbon_fiber/nft_2120.glb"
uv_nft = "C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/uv_gltfs/Kadcar_UV.glb"
hdri = "C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/hdr_files/storage_background.exr"
sticker = "C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/textures/wiz.png"
# nft = "C:/Users/Mohannad Ahmad/Desktop/nft_1.glb"
# uv_nft = "C:/Users/Mohannad Ahmad/Desktop/Kadcar_UV.glb"
# hdri = "C:/Users/Mohannad Ahmad\Desktop/AppDev/Crypto/Kadena\KadcarBackendApi/kadcars_backend_api_local_bpy/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/hdr_files/beach_background.hdr"
# sticker = "C:/Users/Mohannad Ahmad/Desktop/AppDev/Kadena/kadcars_backend/kadcars_backend_api/kadcarsnft_api/NFTFusion/assets/textures/wiz.png"

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
    #import the main car
    import_scene_into_collection(nft, 'kadcar')

    #import the UV car
    import_scene_into_collection(uv_nft, 'uv_kadcar')

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

def copy_uv_maps_from_source():
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

    bsdf = get_principled_bsdf_for_active_material(og_kadcar_body)
    kadcar_color = get_input_value_from_bsdf(bsdf, 'Base Color')
    metallic_value = get_input_value_from_bsdf(bsdf, 'Metallic')
    
    node_tree = get_node_tree_for_selected_object(og_kadcar_body)
    nodes = node_tree.nodes

    texture_node = nodes.new("ShaderNodeTexImage")
    texture_node.image = bpy.data.images.load(sticker)
    texture_node.name = "STICKER_NODE"

    #UV Map Setting
    uv_node = nodes.new("ShaderNodeUVMap")
    uv_node.uv_map = "UVMap.002"
    uv_node.name = "UV_MAP_NODE"

    mix_node = nodes.new("ShaderNodeMixRGB")
    mix_node.inputs['Color1'].default_value = kadcar_color
    mix_node.name = "MIX_NODE"

    node_tree.links.new(uv_node.outputs['UV'], texture_node.inputs['Vector'])
    node_tree.links.new(texture_node.outputs['Color'], mix_node.inputs['Color2'])
    node_tree.links.new(texture_node.outputs['Alpha'], mix_node.inputs['Fac'])
    node_tree.links.new(mix_node.outputs['Color'], bsdf.inputs['Base Color'])

    #Baking
    deselect_all_scene_objects()
    bsdf.inputs['Metallic'].default_value = 0.0
    
    configure_bake_settings('CYCLES', 'CUDA', 'GPU', False, False, False, 'DIFFUSE')
    
    uv_layers = og_kadcar_body.data.uv_layers
    uv_layer_names = [uv.name for uv in uv_layers]
    for name in uv_layer_names:
        if name == "UVMap":
            uv_layers[name].active = True
            print(name)
            print(uv_layers[name])

    image_name = "baked_texture_image"
    image = bpy.data.images.new(image_name, 4096, 4096)
    bake_texture_node = nodes.new("ShaderNodeTexImage")
    bake_texture_node.select = True
    bake_texture_node.name = "BAKED_TEXTURE"
    nodes.active = bake_texture_node
    bake_texture_node.image = image
    
    select_object_by_name_and_make_active('Car_Body')
    
    print(bpy.context.view_layer.objects.active)
    print(uv_layers.active)

    bpy.ops.object.bake('INVOKE_DEFAULT', type='DIFFUSE', pass_filter={'COLOR'}, save_mode='EXTERNAL', target='IMAGE_TEXTURES')

    for node in nodes:
        print(node.name)
        if node.name not in permanent_node_names:
            nodes.remove(node)
    
    node_tree.links.new(bake_texture_node.outputs['Color'], bsdf.inputs['Base Color'])
    set_input_value_in_bsdf(bsdf, 'Metallic', metallic_value)

    export_scene_as_gltf('K:/test_uv.glb')

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