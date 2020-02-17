from typing import Callable

from flask import Response

RouteHandler = Callable[..., Response]

__all__ = ["RouteHandler"]
