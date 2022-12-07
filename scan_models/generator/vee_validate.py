from scan_models.generator.scan_field import ScanFieldGenerator


class VeeValidateGenerator(ScanFieldGenerator):
    """
    Vee validate is not supported anymore
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data["validator"] = {}

    def set_required(self):
        self.data["validator"]["required"] = True

    def set_max_length(self, max_length: int):
        self.data["validator"]["max"] = max_length

    def set_choices(self, choices: list):
        self.data["validator"]["oneOf"] = choices

    def set_max_value(self, max_value: float):
        self.data["validator"]["max_value"] = max_value

    def set_min_value(self, min_value: float):
        self.data["validator"]["min_value"] = min_value

    def set_is_email(self):
        self.data["validator"]["email"] = True

    def set_regex(self, regex: str):
        self.data["validator"]["regex"] = regex
