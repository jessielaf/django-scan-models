import json
import os

from scan_models.main import scan_model

standard_output = {
    "name": {"type": "string", "validator": {"max": 30}, "attributes": {}},
    "email": {
        "type": "email",
        "validator": {"required": True, "max": 254, "email": True},
        "attributes": {},
    },
    "max_amount": {
        "type": "number",
        "validator": {"required": True, "max_value": 4},
        "attributes": {},
    },
    "min_amount": {
        "type": "number",
        "validator": {"required": True, "min_value": 1},
        "attributes": {},
    },
    "choices": {
        "type": "array",
        "validator": {
            "required": True,
            "max": 4,
            "oneOf": ["yes", "no"],
        },
        "attributes": {"options": ["Yes", "No"]},
    },
    "a_or_b": {
        "type": "string",
        "validator": {"max": 200, "regex": "(a|b)"},
        "attributes": {},
    },
    "test_one": {"type": "string", "attributes": {}, "validator": {"required": True}},
    "test_many": {"type": "array", "attributes": {}, "validator": {}},
}


def create_test(model):
    path = "./test_output/output.json"
    scan_model(model, path)

    file = open(os.path.abspath(path), "r")
    data = json.load(file)

    return data
