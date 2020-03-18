import json
import os

from django.apps import apps

from scan_models.parser import FieldParser


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
            validator[_snake_to_camel(field.name)] = validator_field

    with open(os.path.abspath(output), "w") as outfile:
        json.dump(validator, outfile, indent=2)


def _snake_to_camel(value: str):
    """
    Snake casing to camel

    Args:
        value: The string to format
    """
    components = value.split("_")
    return components[0] + "".join(x.title() for x in components[1:])
