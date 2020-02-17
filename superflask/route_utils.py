from functools import wraps
from typing import Any, Dict, Optional, List, Callable, Tuple

from flask import Response
import flasgger

from .types import RouteHandler


def route_factory() -> Tuple[
    List[Tuple[Dict[str, Any], RouteHandler]],
    Callable[..., Callable[[RouteHandler], RouteHandler]],
]:
    routes: List[Tuple[Dict[str, Any], RouteHandler]] = []

    def route(
        rule: str, methods: Optional[List[str]] = None, **kw: Any
    ) -> Callable[[RouteHandler], RouteHandler]:
        dct: Dict[str, Any] = {"rule": rule, **kw}
        if methods is not None:
            dct["methods"] = methods

        def route__decorator(func: RouteHandler) -> RouteHandler:
            routes.append((dct, func))
            return func

        return route__decorator

    return routes, route


def swagger_factory(swagger_path: str) -> Callable[[str], Callable[[RouteHandler], RouteHandler]]:
    def swagger_from(path: str) -> Callable[[RouteHandler], RouteHandler]:
        path = path.strip("/")

        def swag_from__decorator(func: RouteHandler) -> RouteHandler:
            @wraps(func)
            @flasgger.swag_from(f"{swagger_path}/{path}")
            def _wrapper(*a: Any, **kw: Any) -> Response:
                return func(*a, **kw)

            return _wrapper

        return swag_from__decorator

    return swagger_from
