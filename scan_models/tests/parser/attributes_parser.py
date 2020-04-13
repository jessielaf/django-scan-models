from collections import OrderedDict

from django.conf import settings
from django.db.models import fields, Choices
from django.test import TestCase

from scan_models.parser.attributes import AttributesParser
from scan_models.settings import DEFAULT_SETTINGS

od = OrderedDict()


class TestAttributesParser(TestCase):
    def test_nothing(self):
        self.assertEqual(od, AttributesParser(fields.CharField()).parse())

    def test_type(self):
        self.assertEqual({"type": "number"}, AttributesParser(fields.IntegerField()).parse())
        self.assertEqual({"type": "email"}, AttributesParser(fields.EmailField()).parse())

    def test_element(self):
        # Check if it is not added when verbosity is not high enough
        self.assertEqual({}, AttributesParser(fields.BooleanField()).parse())
        self.assertEqual({}, AttributesParser(fields.TextField()).parse())

        # Check if added if verbosity is high enough
        settings.SCAN_MODELS["verbosity"] = 2
        self.assertEqual({"element": "checkbox"}, AttributesParser(fields.BooleanField()).parse())
        self.assertEqual({"element": "textarea"}, AttributesParser(fields.TextField()).parse())

        # Reset verbosity
        settings.SCAN_MODELS["verbosity"] = DEFAULT_SETTINGS["verbosity"]

    def test_choices(self):
        class TestChoices(Choices):
            YES = "wat"
            NO = "test"

        self.assertEqual(
            {"options": ["Yes", "No"]}, AttributesParser(fields.CharField(choices=TestChoices.choices)).parse()
        )
