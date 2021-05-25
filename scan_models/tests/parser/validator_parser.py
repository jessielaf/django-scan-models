from collections import OrderedDict
from unittest.mock import MagicMock

from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, URLValidator
from django.db import models
from django.test import TestCase

from scan_models.parser.validator import ValidatorParser

od = OrderedDict()


class TestValidatorParser(TestCase):
    def test_skip_auto(self):
        parser = ValidatorParser(models.AutoField())
        self.assertFalse(bool(parser.parse()))

    def test_required(self):
        parser = ValidatorParser(models.CharField())
        set_required = MagicMock()
        parser.validator_class.set_required = set_required

        # Test basic CharField
        parser._calculate_required()
        self.assertTrue(set_required.called)
        set_required.reset_mock()

        # Check with null set to true
        parser.field = models.CharField(null=True)
        parser._calculate_required()
        self.assertFalse(set_required.called)
        set_required.reset_mock()

        # Check with blank set to true
        parser.field = models.CharField(blank=True)
        parser._calculate_required()
        self.assertFalse(set_required.called)
        set_required.reset_mock()

        # Check with a default set
        parser.field = models.CharField(default="")
        parser._calculate_required()
        self.assertFalse(set_required.called)
        set_required.reset_mock()

    def test_max_length(self):
        parser = ValidatorParser(models.CharField(max_length=44))
        set_max_length = MagicMock()
        parser.validator_class.set_max_length = set_max_length

        parser._calculate_max_length()
        set_max_length.assert_called_with(od, 44)
        set_max_length.reset_mock()

        parser.field = models.IntegerField()
        parser._calculate_max_length()
        self.assertFalse(set_max_length.called)
        set_max_length.reset_mock()

    def test_choices(self):
        class ChoiceClass(models.Choices):
            FIRST = "first"
            SECOND = "second"

        parser = ValidatorParser(models.CharField(choices=ChoiceClass.choices))
        set_choices = MagicMock()
        parser.validator_class.set_choices = set_choices

        # Test with choices
        parser._calculate_choices()
        set_choices.assert_called_with(od, ["first", "second"])
        set_choices.reset_mock()

        parser.field = models.CharField()
        parser._calculate_choices()
        self.assertFalse(set_choices.called)
        set_choices.reset_mock()

    def test_email(self):
        parser = ValidatorParser(models.CharField())
        set_is_email = MagicMock()
        parser.validator_class.set_is_email = set_is_email

        parser._calculate_email()
        self.assertFalse(set_is_email.called)
        set_is_email.reset_mock()

        parser.field = models.EmailField()
        parser._calculate_email()
        self.assertTrue(set_is_email.called)
        set_is_email.reset_mock()

    def test_regex(self):
        parser = ValidatorParser(models.CharField())
        set_regex = MagicMock()
        parser.validator_class.set_regex = set_regex

        parser._calculate_regex()
        self.assertFalse(set_regex.called)
        set_regex.reset_mock()

        parser.field = models.CharField(validators=[RegexValidator(regex=r"(a|b)")])

        parser._calculate_regex()
        self.assertTrue(set_regex.called)
        set_regex.reset_mock()

        parser.field = models.CharField(validators=[URLValidator()])

        parser._calculate_regex()
        self.assertTrue(set_regex.called)
        set_regex.reset_mock()

        parser.field = models.CharField(validators=[RegexValidator(regex=r"^[\w.@+-]+\Z")])

        parser._calculate_regex()
        set_regex.assert_called_with(parser.validator, r"^[\w.@+-]+$")
        set_regex.reset_mock()

    def test_max_min_value(self):
        parser = ValidatorParser(models.CharField())
        set_max_value = MagicMock()
        parser.validator_class.set_max_value = set_max_value

        set_min_value = MagicMock()
        parser.validator_class.set_min_value = set_min_value

        parser._calculate_max_min_value()
        self.assertFalse(set_max_value.called)
        set_max_value.reset_mock()
        self.assertFalse(set_min_value.called)
        set_min_value.reset_mock()

        parser.field = models.IntegerField()
        parser._calculate_max_min_value()
        self.assertFalse(set_max_value.called)
        set_max_value.reset_mock()
        self.assertFalse(set_min_value.called)
        set_min_value.reset_mock()

        parser.field = models.IntegerField(validators=[MinValueValidator(3), MaxValueValidator(5)])
        parser._calculate_max_min_value()
        set_max_value.assert_called_with(od, 5)
        set_max_value.reset_mock()
        set_min_value.assert_called_with(od, 3)
        set_min_value.reset_mock()
