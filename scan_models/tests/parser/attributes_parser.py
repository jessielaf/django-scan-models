from collections import OrderedDict

from django.db.models import fields, Choices
from django.test import TestCase

from scan_models.parser.attributes import AttributesParser

od = OrderedDict()


class TestAttributesParser(TestCase):
    def test_nothing(self):
        self.assertEqual(od, AttributesParser(fields.CharField()).parse())

    def test_number(self):
        self.assertEqual({"type": "number"}, AttributesParser(fields.IntegerField()).parse())

    def test_email(self):
        self.assertEqual({"type": "email"}, AttributesParser(fields.EmailField()).parse())

    def test_choices(self):
        class TestChoices(Choices):
            YES = "wat"
            NO = "test"

        self.assertEqual(
            {"options": ["Yes", "No"]}, AttributesParser(fields.CharField(choices=TestChoices.choices)).parse()
        )
