import json
import os
from copy import copy

from django.conf import settings
from django.test import TestCase

from scan_models.main import scan_model
from scan_models.settings import DEFAULT_SETTINGS
from scan_models.tests.constances import standard_output


class TestHappyFlow(TestCase):
    def setUp(self) -> None:
        settings.SCAN_MODELS = copy(DEFAULT_SETTINGS)

    def create_test(self):
        path = "./output.json"
        scan_model("tests.TestModel", path)

        file = open(os.path.abspath(path), "r")
        data = json.load(file)

        return data

    def test_happy_flow(self):
        data = self.create_test()
        self.assertEqual(data, standard_output)

    def test_camelize(self):
        settings.SCAN_MODELS["camelize"] = True
        output = copy(standard_output)

        output["maxAmount"] = output.pop("max_amount")
        output["minAmount"] = output.pop("min_amount")

        data = self.create_test()
        self.assertEqual(data, output)
