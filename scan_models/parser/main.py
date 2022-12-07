from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db.models import fields

from scan_models.factory import Factory
from scan_models.field_helpers import is_many
from scan_models.generator.base_generator import BaseGenerator


class FieldParser:
    generator: BaseGenerator

    def __init__(self, field: fields.Field):
        self.field = field
        self.generator = Factory.get_validator()(field)
        super().__init__()

    def parse(self):
        # If auto field there is no frontend validation
        if isinstance(self.field, fields.AutoField):
            return None

        if not is_many(self.field):
            self._calculate_required()
            self._calculate_max_length()
            self._calculate_choices()
            self._calculate_max_min_value()
            self._calculate_email()
            self._calculate_regex()

        self.generator.parse()

        return self.generator.data

    def _calculate_required(self):
        required = (
            self.field.default == fields.NOT_PROVIDED
            and not self.field.blank
            and not self.field.null
        )

        if required:
            self.generator.set_required()

    def _calculate_email(self):
        if isinstance(self.field, fields.EmailField):
            self.generator.set_is_email()

    def _calculate_max_length(self):
        if self.field.max_length:
            self.generator.set_max_length(self.field.max_length)

    def _calculate_choices(self):
        if self.field.choices:
            self.generator.set_choices([choice[0] for choice in self.field.choices])

    def _calculate_regex(self):
        regex_validator = self._find_validator(RegexValidator)

        if regex_validator:
            pattern = regex_validator.regex.pattern

            pattern = pattern.replace("\\Z", "$")

            self.generator.set_regex(pattern)

    def _calculate_max_min_value(self):
        if not isinstance(self.field, fields.IntegerField):
            return

        max_validator = self._find_validator(MaxValueValidator)
        min_validator = self._find_validator(MinValueValidator)

        internal_type = self.field.get_internal_type()
        min_value, max_value = fields.connection.ops.integer_field_range(internal_type)

        if max_validator and max_validator.limit_value != max_value:
            self.generator.set_max_value(max_validator.limit_value)

        if min_validator and min_validator.limit_value != min_value:
            self.generator.set_min_value(min_validator.limit_value)

    def _find_validator(self, validator_class):
        validator = [
            validator
            for validator in self.field.validators
            if isinstance(validator, validator_class)
        ]

        return validator[0] if len(validator) else None
