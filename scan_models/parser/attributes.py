from collections import OrderedDict

from django.db.models import fields


class AttributesParser:
    def __init__(self, field: fields.Field):
        self.field = field
        self.attributes = OrderedDict()

    def parse(self):
        self._calculate_element()
        self._calculate_type()
        self._calculate_options()

        return self.attributes

    def _calculate_element(self):
        element = ""

        if isinstance(self.field, fields.TextField):
            element = "textarea"
        if isinstance(self.field, fields.BooleanField):
            element = "checkbox"

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
        if self.field.choices:
            self.attributes["options"] = [choice[1] for choice in self.field.choices]
