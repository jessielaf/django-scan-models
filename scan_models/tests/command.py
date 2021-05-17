import json
import os
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from scan_models.tests.constances import standard_output


class TestCommand(TestCase):
    maxDiff = None

    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            "scan_models",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    def test_all_models(self):
        self.call_command()

        with open(os.path.abspath("test_output/output.json"), "r") as file:
            self.assertEqual(standard_output, json.load(file))

    def test_location_prefix(self):
        self.call_command(prefix="test_output")

        # Double test output because extra prefix
        with open(os.path.abspath("test_output/test_output/output.json"), "r") as file:
            self.assertEqual(standard_output, json.load(file))
