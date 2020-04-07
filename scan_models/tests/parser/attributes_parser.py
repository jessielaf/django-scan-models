from collections import OrderedDict

from django.db.models import fields, Choices
from django.test import TestCase

from scan_models.parser.attributes import AttributesParser

od = OrderedDict()


class TestAttributesParser(TestCase):
    def test_nothing(self):
        self.assertEqual(od, AttributesParser(fields.CharField()).parse())

    def test_type(self):
        self.assertEqual({"type": "number"}, AttributesParser(fields.IntegerField()).parse())
        self.assertEqual({"type": "email"}, AttributesParser(fields.EmailField()).parse())

    def test_element(self):
        self.assertEqual({"element": "checkbox"}, AttributesParser(fields.BooleanField()).parse())
        self.assertEqual({"element": "textarea"}, AttributesParser(fields.TextField()).parse())

    def test_choices(self):
        class TestChoices(Choices):
            YES = "wat"
            NO = "test"

        self.assertEqual(
            {"options": ["Yes", "No"]}, AttributesParser(fields.CharField(choices=TestChoices.choices)).parse()
        )
