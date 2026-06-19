import json


def load_kit_file(path):
    with open(path, "r") as file:
        return json.load(file)
