from collections import OrderedDict

from django.db.models import Field, fields


class BaseGenerator:
    field: Field

    def __init__(self, field: fields.Field):
        self.data = OrderedDict()
        self.field = field

    def parse(self):
        """
        With this function you can manipulate the data object outside of the set functions
        """
        pass

    def set_required(self):
        pass

    def set_max_length(self, max_length: int):
        pass

    def set_choices(self, choices: list):
        pass

    def set_max_value(self, max_value: float):
        pass

    def set_min_value(self, min_value: float):
        pass

    def set_is_email(self):
        pass

    def set_regex(self, regex: str):
        pass
