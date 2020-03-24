import json
import os
from copy import deepcopy

from django.conf import settings
from django.test import TestCase

from scan_models.main import scan_model

response = {
    "name": {"validator": {"max": 30}},
    "email": {"validator": {"required": True, "email": True, "max": 254}},
    "max_amount": {"validator": {"max_value": 4, "required": True}, "attributes": {"type": "number"}},
    "min_amount": {"validator": {"min_value": 1, "required": True}, "attributes": {"type": "number"}},
}

base_settings = deepcopy(settings)


class TestHappyFlow(TestCase):
    def create_test(self):
        path = "./output.json"
        scan_model("tests.TestModel", path)

        file = open(os.path.abspath(path), "r")
        data = json.load(file)

        return data

    def test_happy_flow(self):
        data = self.create_test()
        self.assertEqual(data, response)

    def test_camelize(self):
        settings.SCAN_MODELS["camelize"] = True

        response["maxAmount"] = response.pop("max_amount")
        response["minAmount"] = response.pop("min_amount")

        data = self.create_test()
        self.assertEqual(data, response)
