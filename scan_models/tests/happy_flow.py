import json
from copy import copy

from django.conf import settings
from django.test import TestCase

from scan_models.settings import DEFAULT_SETTINGS
from scan_models.tests.constances import standard_output, create_test


class TestHappyFlow(TestCase):
    def setUp(self) -> None:
        settings.SCAN_MODELS = copy(DEFAULT_SETTINGS)

    def test_happy_flow(self):
        data = create_test("tests.TestModel")
        self.assertEqual(data, standard_output)

    def test_camelize(self):
        settings.SCAN_MODELS["camelize"] = True
        output = copy(standard_output)

        output["maxAmount"] = output.pop("max_amount")
        output["minAmount"] = output.pop("min_amount")

        data = create_test("tests.TestModel")
        self.assertEqual(data, output)
