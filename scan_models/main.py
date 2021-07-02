import json
import os
from pathlib import Path

from django.apps import apps

from scan_models.parser.main import FieldParser
from scan_models.settings import get_setting


def scan_model(model_name: str, output: str, location_prefix: str = ""):
    """
    Scan the model and output it to a file

    Args:
        model_name (str): The name of the model. Preferably with the app. Example: companies.Company
        output (str): Output file. Advised to use .json on the end
    """

    validator = {}

    model_meta = apps.get_model(model_name)._meta

    # Also add related objects and many to many objects
    fields = list(model_meta.many_to_many) + list(model_meta.related_objects) + list(model_meta.fields)

    for field in fields:
        validator_field = FieldParser(field).parse()

        if validator_field:
            validator[_format_name(field.name)] = validator_field

    # We need to make sure the directory where we put the file exists
    location_prefix = Path(location_prefix or "")
    output_path = location_prefix.joinpath(Path(output))
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)

    with open(output_path.resolve(), "w") as outfile:
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
