from functools import wraps
from typing import Any, Callable, Iterable

from flask import Response, request

from .exceptions import MissingParameters, NoPayloadDetected
from .types import RouteHandler


def with_payload(
    required: Iterable[str] = (),
) -> Callable[[RouteHandler], RouteHandler]:
    """
    Handle POST json body retrieval, extract required keys
    and pass the key-values and the payload to the route handler
    """

    def _with_payload_decorator(func: RouteHandler) -> RouteHandler:
        @wraps(func)
        def _wrapper(*a: Any, **kw: Any) -> Response:
            json = request.json
            if json is None:
                raise NoPayloadDetected()
            vals = {}
            missing = set()
            for key in required:
                try:
                    vals[key] = json[key]
                except KeyError:
                    missing.add(key)
            if missing:
                raise MissingParameters(missing)
            return func(*a, payload=json, **kw, **vals)

        return _wrapper

    return _with_payload_decorator


def from_json(*keys: str) -> Callable[[RouteHandler], RouteHandler]:
    """
    Extract particular keys from POST request's json payload
    and pass them as keyword arguments to the route handler
    """

    def _from_json_decorator(func: RouteHandler) -> RouteHandler:
        @wraps(func)
        def _wrapper(*a: Any, **kw: Any) -> Response:
            json = request.json
            if json is None:
                raise NoPayloadDetected()
            vals = {}
            missing = set()
            for key in keys:
                try:
                    vals[key] = json[key]
                except KeyError:
                    missing.add(key)
            if missing:
                raise MissingParameters(missing)
            return func(*a, **kw, **vals)

        return _wrapper

    return _from_json_decorator
