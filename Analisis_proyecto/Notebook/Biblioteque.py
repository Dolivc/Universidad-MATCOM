import json

path = "./Json/mipymes.json"

def open_json(path):  
    with open(path, "r", encoding='utf-8') as j:
        data = json.load(j)
    return data

