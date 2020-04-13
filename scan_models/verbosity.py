from enum import Enum

from scan_models.settings import get_setting


class Verbosity(Enum):
    ONE = 1
    TWO = 2


def is_verbosity(verbosity: Verbosity):
    return verbosity.value <= get_setting("verbosity")
