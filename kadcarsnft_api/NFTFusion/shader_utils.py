import bpy

def get_principled_bsdf_for_material(material_name):
    material = bpy.data.materials[material_name]
    material.use_nodes = True
    tree = material.node_tree
    nodes = tree.nodes
    bsdf = nodes["Principled BSDF"]

    return bsdf

def transfer_materials_bulk(clean, src, target_list):
    for tgt in target_list:
        transfer_materials(clean, src, tgt)

def transfer_materials(clean, src, tgt):
    if clean:
        tgt.data.materials.clear() # ensure the target material slots are clean
    
    for mat in src.data.materials:
        tgt.data.materials.append(mat)

def add_material():
    pass