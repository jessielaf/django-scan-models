from collections import OrderedDict

from django.db.models import fields, ManyToManyField, IntegerField
from django.test import TestCase

from scan_models.parser.main import FieldParser
from tests.models import TestModel

od = OrderedDict()


class TestAttributesParser(TestCase):
    def test_element(self):
        # Checkbox
        parser = FieldParser(fields.BooleanField())
        self.assertEqual("boolean", parser.parse()["type"])

        # TextArea
        parser = FieldParser(fields.TextField())
        self.assertEqual("textfield", parser.parse()["type"])

        # Date
        parser = FieldParser(fields.DateField())
        self.assertEqual("date", parser.parse()["type"])

        # Select
        parser = FieldParser(fields.CharField(choices=(("1", "1"), ("2", "2"))))
        self.assertEqual("array", parser.parse()["type"])

        # Many to many
        parser = FieldParser(ManyToManyField(TestModel))
        self.assertEqual("array", parser.parse()["type"])

        # Many to many
        parser = FieldParser(IntegerField(TestModel))
        self.assertEqual("int", parser.parse()["type"])
