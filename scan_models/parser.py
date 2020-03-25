from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import fields

from scan_models.validators.base_validator import BaseValidator
from scan_models.validators.factory import ValidatorFactory


class FieldParser:
    field: fields.Field
    validator = {}
    validator_class: BaseValidator

    def __init__(self, field: fields.Field):
        self.validator_class = ValidatorFactory.get_validator()()
        self.field = field

        super().__init__()

    def parse(self):
        # If auto field there is no frontend validation
        if isinstance(self.field, fields.AutoField):
            return None

        parsed = {}

        self.validator = {}
        self._parse_validator()
        if self.validator:
            parsed["validator"] = self.validator

        attributes = self._parse_attributes()
        if attributes:
            parsed["attributes"] = attributes

        return parsed

    def _parse_attributes(self):
        attributes = {}
        if isinstance(self.field, fields.IntegerField):
            attributes["type"] = "number"

        return attributes

    def _parse_validator(self):
        self._calculate_required()
        self._calculate_email()
        self._calculate_max_length()
        self._calculate_max_min_value()

    def _calculate_required(self):
        required = self.field.default == fields.NOT_PROVIDED and not self.field.blank and not self.field.null

        if required:
            self.validator_class.set_required(self.validator)

    def _calculate_email(self):
        if isinstance(self.field, fields.EmailField):
            self.validator_class.set_is_email(self.validator)

    def _calculate_max_length(self):
        if self.field.max_length:
            self.validator_class.set_max_length(self.validator, self.field.max_length)

    def _calculate_max_min_value(self):
        if not isinstance(self.field, fields.IntegerField):
            return

        max_validator = [validator for validator in self.field.validators if isinstance(validator, MaxValueValidator)]
        min_validator = [validator for validator in self.field.validators if isinstance(validator, MinValueValidator)]

        internal_type = self.field.get_internal_type()
        min_value, max_value = fields.connection.ops.integer_field_range(internal_type)

        if len(max_validator):
            max_validator_value = max_validator[0].limit_value
            if max_validator_value != max_value:
                self.validator_class.set_max_value(self.validator, max_validator_value)

        if len(min_validator):
            min_validator_value = min_validator[0].limit_value
            if min_validator_value != min_value:
                self.validator_class.set_min_value(self.validator, min_validator_value)
