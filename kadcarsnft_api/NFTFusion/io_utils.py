import os
import json

def extract_data_from_json(json_file):
    dirname = os.path.dirname(__file__)
    json_path = os.path.join(dirname, json_file)

    f = open(json_path)
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
    with open(os.path.join(dirname, "json_config_files/" + output + ".json"), "w") as outfile:
        json.dump(dictionary, outfile)