import os

SCRIPT_LOC = os.path.dirname(os.path.realpath(__file__))
ROOT = f"{SCRIPT_LOC}/.."


class colors:
    red: str = "\033[31m"
    green: str = "\033[32m"
    blue: str = "\033[34m"
    reset: str = "\033[0m"
