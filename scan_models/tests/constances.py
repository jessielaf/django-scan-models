import json
import os

from scan_models.main import scan_model

standard_output = {
    "name": {"validator": {"max": 30}},
    "email": {"validator": {"required": True, "max": 254, "email": True}, "attributes": {"type": "email"}},
    "max_amount": {"validator": {"required": True, "max_value": 4}, "attributes": {"type": "number"}},
    "min_amount": {"validator": {"required": True, "min_value": 1}, "attributes": {"type": "number"}},
    "choices": {
        "validator": {"required": True, "max": 4, "oneOf": ["yes", "no"]},
        "attributes": {"options": ["Yes", "No"]},
    },
}


def create_test(model):
    path = "./output.json"
    scan_model(model, path)

    file = open(os.path.abspath(path), "r")
    data = json.load(file)

    return data
