from kadcar_factory import get_color_name

def update_metadata_stat(kadcar_metadata, primary, secondary, value):
    for metadata in kadcar_metadata:
        if metadata["name"] == primary:
            for stat in metadata["mutable-state"]:
                if stat["key"] == secondary:
                    stat["val"] = value

def update_visual_stat_type_and_id_in_metadata(kadcar_metadata_components, kadcar_specs, part, type, stat_val_id):
    for metadata in kadcar_metadata_components:
        for stat in metadata["mutable-state"]:
            if stat["key"] == str(part + "-material"):
                stat["val"]["type"] = type
                    
                if part == 'Car_Body':
                    stat_val_id = get_color_name(kadcar_specs['Color'])

                # stat["val"]["id"] = kadcar_specs['Material'] + "-" + kadcar_specs['Color']
                stat["val"]["id"] = stat_val_id

def update_metadata_entry(metadata, keys_array, value):
    destination_key = None

    for i in range(len(keys_array)):
        if i == 0:
            destination_key = metadata[keys_array[i]]
        
        destination_key = destination_key[keys_array[i]]
    
    destination_key = value

    return metadata