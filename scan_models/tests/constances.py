import json
import os

from scan_models.main import scan_model

standard_output = {
    "name": {"validator": {"max": 30}, "attributes": {}},
    "email": {"validator": {"required": True, "max": 254, "email": True}, "attributes": {"type": "email"}},
    "max_amount": {"validator": {"required": True, "max_value": 4}, "attributes": {"type": "number"}},
    "min_amount": {"validator": {"required": True, "min_value": 1}, "attributes": {"type": "number"}},
    "choices": {
        "validator": {"required": True, "max": 4, "oneOf": ["yes", "no"]},
        "attributes": {"options": ["Yes", "No"], "element": "select"},
    },
    "a_or_b": {"validator": {"max": 200, "regex": "(a|b)"}, "attributes": {}},
    "test_one": {"attributes": {}, "validator": {"required": True}},
    "test_many": {"attributes": {"element": "select"}, "validator": {}},
}


def create_test(model):
    path = "./test_output/output.json"
    scan_model(model, path)

    file = open(os.path.abspath(path), "r")
    data = json.load(file)

    return data
