import uuid
from collections import OrderedDict
from unittest.mock import MagicMock

from django.conf import settings
from django.db.models import fields, Choices, ManyToManyField
from django.test import TestCase

from scan_models.parser.attributes import AttributesParser
from scan_models.settings import DEFAULT_SETTINGS
from tests.models import TestModel

od = OrderedDict()


class TestAttributesParser(TestCase):
    def test_nothing(self):
        self.assertEqual(od, AttributesParser(fields.CharField()).parse())

    def test_function_calls(self):
        parser = AttributesParser(fields.CharField())
        parser._calculate_options = MagicMock()
        parser._calculate_element = MagicMock()
        parser._calculate_type = MagicMock()
        parser._calculate_default = MagicMock()

        parser.parse()

        self.assertEqual(parser._calculate_options.call_count, 1)
        self.assertEqual(parser._calculate_type.call_count, 1)
        self.assertEqual(parser._calculate_default.call_count, 1)

    def test_type(self):
        # Number type
        parser = AttributesParser(fields.IntegerField())
        parser._calculate_type()
        self.assertEqual("number", parser.attributes["type"])

        # Email type
        parser = AttributesParser(fields.EmailField())
        parser._calculate_type()
        self.assertEqual("email", parser.attributes["type"])

        # Array type
        parser = AttributesParser(ManyToManyField(TestModel))
        parser._calculate_type()
        self.assertEqual("email", parser.attributes["type"])

    def test_element(self):
        # Email type
        parser = AttributesParser(fields.TextField())
        parser._calculate_element()
        self.assertEqual("textfield", parser.attributes["element"])

    def test_options(self):
        class TestChoices(Choices):
            YES = "wat"
            NO = "test"

        parser = AttributesParser(fields.CharField(choices=TestChoices.choices))
        parser._calculate_options()
        self.assertEqual(["Yes", "No"], parser.attributes["options"])

    def test_default(self):
        parser = AttributesParser(fields.CharField())
        parser._calculate_default()
        self.assertFalse("default" in parser.attributes)

        parser = AttributesParser(fields.CharField(default=""))
        parser._calculate_default()
        self.assertFalse("default" in parser.attributes)

        parser = AttributesParser(fields.CharField(default="test"))
        parser._calculate_default()
        self.assertEqual("test", parser.attributes["default"])

        parser = AttributesParser(fields.CharField(default=uuid.uuid4()))
        parser._calculate_default()
        self.assertFalse("default" in parser.attributes)
