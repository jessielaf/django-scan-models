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
