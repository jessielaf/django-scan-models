import json
import os

from django.test import TestCase

from scan_models.management.commands.scan_models import Command
from scan_models.tests.constances import standard_output


class TestCommand(TestCase):
    def test_all_models(self):
        Command().handle()

        with open(os.path.abspath("./output.json"), "r") as file:
            self.assertEqual(standard_output, json.load(file))
