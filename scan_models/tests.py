import json
import os

from django.test import TestCase

from scan_models.main import scan_model


class TestScanModel(TestCase):
    def test_happy_flow(self):
        path = "./output.json"
        scan_model("tests.TestModel", path)

        with open(os.path.abspath(path), "r") as file:
            data = json.load(file)
            response = {
                "name": {"validator": {"max": 30}},
                "email": {"validator": {"required": True, "email": True, "max": 254}},
                "maxAmount": {"validator": {"required": True}, "attributes": {"type": "number"}},
                "minAmount": {"validator": {"required": True}, "attributes": {"type": "number"}},
            }

            self.assertEqual(data, response)
