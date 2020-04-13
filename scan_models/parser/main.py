from django.db.models import fields

from scan_models.parser.attributes import AttributesParser
from scan_models.parser.validator import ValidatorParser
from scan_models.validators.base_validator import BaseValidator
from scan_models.verbosity import is_verbosity, Verbosity


class FieldParser:
    field: fields.Field
    validator_class: BaseValidator

    def __init__(self, field: fields.Field):
        self.field = field

        super().__init__()

    def parse(self):
        # If auto field there is no frontend validation
        if isinstance(self.field, fields.AutoField):
            return None

        parsed = {}

        validator = ValidatorParser(self.field).parse()
        if validator or is_verbosity(Verbosity.ONE):
            parsed["validator"] = validator

        attributes = AttributesParser(self.field).parse()
        if attributes or is_verbosity(Verbosity.ONE):
            parsed["attributes"] = attributes

        return parsed
