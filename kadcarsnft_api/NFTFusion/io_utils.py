import json

def extract_data_from_json(json_file):
    f = open(json_file)
    data = json.load(f)
    f.close()

    return data