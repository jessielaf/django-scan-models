from copy import copy
from pprint import pprint

from django.conf import settings
from django.test import TestCase

from scan_models.settings import DEFAULT_SETTINGS
from scan_models.tests.constances import standard_output, create_test


class TestHappyFlow(TestCase):
    maxDiff = None

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
        output["aOrB"] = output.pop("a_or_b")
        output["testMany"] = output.pop("test_many")
        output["testOne"] = output.pop("test_one")

        data = create_test("tests.TestModel")
        self.assertEqual(data, output)

    def test_many_to_many_reverse(self):
        data = create_test("tests.TestManyToMany")
        output = {"many_to_many": {"attributes": {"element": "select"}, "validator": {}}}
        self.assertEqual(data, output)

    def test_one_to_many_reverse(self):
        data = create_test("tests.TestOneToMany")
        output = {"one_to_many": {"attributes": {"element": "select"}, "validator": {}}}
        self.assertEqual(data, output)
