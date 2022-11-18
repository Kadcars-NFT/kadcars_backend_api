import os
import json

def extract_data_from_json(json_file):
    f = open(json_file)
    data = json.load(f)
    f.close()

    return data

def extract_json_attribute_data(json_file, attribute):
    attribute_data = extract_data_from_json(json_file)[attribute]
    return attribute_data

def extract_json_keys(json_file):
    keys = extract_data_from_json(json_file).keys()
    return keys

def export_dictionary_to_json(dictionary, output):
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, output + ".json"), "w") as outfile:
        json.dump(dictionary, outfile)

def remove_dir_at_path(dir_path):
    if os.path.exists(dir_path):
        os.rmdir(dir_path)
        return True
    return False

def create_dir_at_path(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        return True
    return False