from unittest.mock import MagicMock

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.test import TestCase

from scan_models.parser import FieldParser


class TestParser(TestCase):
    def test_skip_auto(self):
        parser = FieldParser(models.AutoField())
        self.assertEqual(parser.parse(), None)

    def test_required(self):
        parser = FieldParser(models.CharField())
        parser.validator_class.set_required = MagicMock()

        parser.validator_class.set_required.assert_called_with(True)

        parser.field = models.CharField(null=True)
        parser._calculate_required()
        parser.validator_class.set_required.assert_called_with(False)

        parser.field = models.CharField(blank=True)
        parser._calculate_required()
        parser.validator_class.set_required.assert_called_with(False)

        parser.field = models.CharField(default="")
        parser._calculate_required()
        parser.validator_class.set_required.assert_called_with(False)

    def test_max_length(self):
        parser = FieldParser(models.CharField(max_length=44))
        parser.validator_class.set_max_length = MagicMock()

        parser._calculate_max_length()
        parser.validator_class.set_max_length.assert_called_with(44)

        parser.field = models.IntegerField()
        parser._calculate_max_length()
        self.assertEqual(parser.validator_class.set_required.call_count, 0)

    def test_email(self):
        parser = FieldParser(models.CharField())
        parser.validator_class.set_is_email = MagicMock()

        parser._calculate_email()
        self.assertEqual(parser.validator_class.set_is_email.call_count, 0)

        parser.field = models.EmailField()
        parser._calculate_email()
        parser.validator_class.set_is_email.assert_called_with()

    def test_max_min_value(self):
        parser = FieldParser(models.CharField())
        parser.validator_class.set_max_value = MagicMock()
        parser.validator_class.set_min_value = MagicMock()

        parser._calculate_max_min_value()
        self.assertEqual(parser.validator_class.set_max_value.call_count, 0)
        self.assertEqual(parser.validator_class.set_min_value.call_count, 0)

        parser.field = models.IntegerField()
        self.assertEqual(parser.validator_class.set_max_value.call_count, 0)
        self.assertEqual(parser.validator_class.set_min_value.call_count, 0)

        parser.field = models.IntegerField(validators=[MinValueValidator(3), MaxValueValidator(5)])
        parser.validator_class.set_min_value.assert_called_with(3)
        parser.validator_class.set_max_value.assert_called_with(5)
