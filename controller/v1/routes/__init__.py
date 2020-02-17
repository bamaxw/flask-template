from flask import Blueprint, Response

from .base import route, routes, swag_from


@route("/health", methods=["GET"])
@swag_from("/healthcheck.yml")
def health() -> Response:
    return Response("ok")


def register_routes(controller: Blueprint) -> None:
    for route_config, route_handler in routes:
        controller.route(**route_config)(route_handler)
