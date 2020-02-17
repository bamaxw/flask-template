from typing import Iterable

from . import BaseResponseError


class NoPayloadDetected(BaseResponseError):
    default_status_code = 400

    def __init__(self) -> None:
        super().__init__("No payload detected")


class MissingParameters(BaseResponseError):
    default_status_code = 400

    def __init__(self, missing: Iterable[str]) -> None:
        missing_str = ", ".join(repr(elem) for elem in set(missing))
        super().__init__(f"Request body must specify: {missing_str!s}")
