from collections import OrderedDict

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import fields

from scan_models.factory import Factory


class ValidatorParser:
    def __init__(self, field: fields.Field):
        self.field = field
        self.validator = OrderedDict()
        self.validator_class = Factory.get_validator()()

    def parse(self):
        self._calculate_required()
        self._calculate_max_length()
        self._calculate_choices()
        self._calculate_max_min_value()
        self._calculate_email()

        return self.validator

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

    def _calculate_choices(self):
        if self.field.choices:
            self.validator_class.set_choices(self.validator, [choice[0] for choice in self.field.choices])

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