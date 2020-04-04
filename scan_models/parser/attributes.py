from collections import OrderedDict

from django.db.models import fields


class AttributesParser:
    def __init__(self, field: fields.Field):
        self.field = field

    def parse(self):
        attributes = OrderedDict()

        if isinstance(self.field, fields.IntegerField):
            attributes["type"] = "number"
        elif isinstance(self.field, fields.EmailField):
            attributes["type"] = "email"

        if self.field.choices:
            attributes["options"] = [choice[1] for choice in self.field.choices]

        return attributes
