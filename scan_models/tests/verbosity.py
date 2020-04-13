from django.conf import settings
from django.test import TestCase

from scan_models.settings import DEFAULT_SETTINGS
from scan_models.tests.constances import create_test


class TestVerbosity(TestCase):
    def test_lowest_verbosity(self):
        self.assertEqual(create_test("tests.TestVerbosity"), {})

    def test_first_verbosity(self):
        settings.SCAN_MODELS["verbosity"] = 1
        self.assertEqual(create_test("tests.TestVerbosity"), {"text": {"attributes": {}, "validator": {}}})
        settings.SCAN_MODELS["verbosity"] = DEFAULT_SETTINGS["verbosity"]

    def test_second_verbosity(self):
        settings.SCAN_MODELS["verbosity"] = 2
        self.assertEqual(
            create_test("tests.TestVerbosity"), {"text": {"attributes": {"element": "textarea"}, "validator": {}}}
        )
        settings.SCAN_MODELS["verbosity"] = DEFAULT_SETTINGS["verbosity"]
