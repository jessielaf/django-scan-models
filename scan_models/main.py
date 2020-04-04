import json
import os

from django.apps import apps

from scan_models.parser.main import FieldParser
from scan_models.settings import get_setting


def scan_model(model_name: str, output: str):
    """
    Scan the model and output it to a file

    Args:
        model_name (str): The name of the model. Preferably with the app. Example: companies.Company
        output (str): Output file. Advised to use .json on the end
    """

    fields = apps.get_model(model_name)._meta.fields

    validator = {}

    for field in fields:
        validator_field = FieldParser(field).parse()

        if validator_field:
            validator[_format_name(field.name)] = validator_field

    with open(os.path.abspath(output), "w") as outfile:
        json.dump(validator, outfile, indent=2)


def _format_name(value: str):
    """
    Format the name of the field

    Args:
        value: The string to format
    """

    if get_setting("camelize"):
        components = value.split("_")
        return components[0] + "".join(x.title() for x in components[1:])
    else:
        return value
