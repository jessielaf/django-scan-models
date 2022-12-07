from datetime import date

from django.db import models


def is_many(field: models.Field):
    return (
        isinstance(field, models.ManyToManyField)
        or isinstance(field, models.ManyToManyRel)
        or isinstance(field, models.ManyToOneRel)
    )


def calculate_type(field: models.Field):
    if is_many(field) or field.choices:
        return list
    elif isinstance(field, models.IntegerField):
        return int
    elif isinstance(field, models.BooleanField):
        return bool
    elif isinstance(field, models.DateField):
        return date
    return str
