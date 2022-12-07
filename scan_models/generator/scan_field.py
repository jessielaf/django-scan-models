from datetime import date

from django.db.models import fields

from scan_models.field_helpers import is_many, calculate_type
from scan_models.generator.base_generator import BaseGenerator
from scan_models.verbosity import is_verbosity, Verbosity


class ScanFieldGenerator(BaseGenerator):
    def parse(self):
        self.data["attributes"] = {}

        self._calculate_options()
        self._calculate_default()
        self._calculate_type()

    def _calculate_element(self):
        element = ""
        if isinstance(self.field, fields.TextField):
            element = "textfield"

        if element:
            self.data["attributes"]["element"] = element

    def _calculate_options(self):
        if not is_many(self.field) and self.field.choices:
            self.data["attributes"]["options"] = [
                choice[1] for choice in self.field.choices
            ]

    def _calculate_default(self):
        """
        Only adds primitive types as default

        TODO: Add more options as default
        """

        if (
            not is_many(self.field)
            and self.field.default
            and self.field.default != fields.NOT_PROVIDED
            and isinstance(self.field.default, (list, int, str, bool, float))
        ):
            self.data["attributes"]["default"] = str(self.field.default)

    def _calculate_type(self):
        # Only calculate element if verbosity is high enough.
        # This is only the case when using the frontend scan-field package
        if not is_verbosity(Verbosity.TWO):
            return

        field_type = calculate_type(self.field)

        str_field_type = "string"
        if isinstance(self.field, fields.EmailField):
            str_field_type = "email"
        elif field_type == list:
            str_field_type = "array"
        elif field_type == int:
            str_field_type = "number"
        elif field_type == bool:
            str_field_type = "boolean"
        elif field_type == date:
            str_field_type = "date"

        self.data["type"] = str_field_type
