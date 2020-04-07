from django.core.management import BaseCommand

from scan_models.main import scan_model
from scan_models.settings import get_setting


class Command(BaseCommand):
    help = "Creates the hour registration for the last week"

    def add_arguments(self, parser):
        parser.add_argument(
            "-m", "--model", help="If you only want to specify one model",
        )

    def handle(self, *args, **kwargs):
        data = get_setting("mapping")
        option_model = kwargs.get("model", None)

        if option_model:
            scan_model(option_model, data[option_model])
        else:
            for model, output in data.items():
                scan_model(model, output)
