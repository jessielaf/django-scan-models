from collections import OrderedDict

from django.db.models import fields, ManyToManyField, ManyToManyRel

from scan_models.parser.parser import GeneralParser
from scan_models.verbosity import is_verbosity, Verbosity


class AttributesParser(GeneralParser):
    def __init__(self, field: fields.Field):
        self.field = field
        self.attributes = OrderedDict()

    def parse(self):
        self._calculate_element()
        self._calculate_type()
        self._calculate_options()
        self._calculate_default()

        return self.attributes

    def _calculate_element(self):
        # Only calculate element if verbosity is high enough.
        # This is only the case when using the general-fields package
        if not is_verbosity(Verbosity.TWO):
            return

        element = ""

        if self.is_many or self.field.choices:
            element = "select"
        elif isinstance(self.field, fields.TextField):
            element = "textarea"
        elif isinstance(self.field, fields.BooleanField):
            element = "checkbox"
        elif isinstance(self.field, fields.DateField):
            element = "date"

        if element:
            self.attributes["element"] = element

    def _calculate_type(self):
        type_attr = ""
        if isinstance(self.field, fields.IntegerField):
            type_attr = "number"
        elif isinstance(self.field, fields.EmailField):
            type_attr = "email"

        if type_attr:
            self.attributes["type"] = type_attr

    def _calculate_options(self):
        if not self.is_many and self.field.choices:
            self.attributes["options"] = [choice[1] for choice in self.field.choices]

    def _calculate_default(self):
        """
        Only adds primitive types as default

        TODO: Add more options as default
        """

        if (
            not self.is_many
            and self.field.default
            and self.field.default != fields.NOT_PROVIDED
            and isinstance(self.field.default, (list, int, str, bool, float))
        ):
            self.attributes["default"] = str(self.field.default)
