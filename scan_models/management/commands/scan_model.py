import json
import os

from django.apps import apps
from django.core.management import BaseCommand

from scan_models.parser import FieldParser


class Command(BaseCommand):
    help = "Creates the hour registration for the last week"

    def add_arguments(self, parser):
        parser.add_argument(
            "--model", help="If you only want to specify one model",
        )

    def handle(self, *args, **options):
        with open(os.path.join(os.getcwd(), "scan.json"), "r", encoding="utf-8") as file:
            data = json.load(file)
            option_model = options.get("model", None)

            if option_model:
                self.scan_model(self.get_model(option_model), data[option_model])
            else:
                for model, output in data.items():
                    self.scan_model(self.get_model(model), output)

    def get_model(self, model_name):
        return apps.get_model(model_name)

    def scan_model(self, model, output):
        fields = model._meta.fields

        validator = {}

        for field in fields:
            vuetifyField = FieldParser(field).parse()

            if vuetifyField:
                validator[self.snake_to_camel(field.name)] = vuetifyField

        with open(os.path.join(os.getcwd(), os.path.abspath(output)), "w") as outfile:
            json.dump(validator, outfile, indent=2)

    def snake_to_camel(self, value: str):
        components = value.split("_")
        return components[0] + "".join(x.title() for x in components[1:])
