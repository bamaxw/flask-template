from typing import Mapping, Optional

from flask import Response, jsonify


class BaseResponseError(Exception):
    """
    BaseResponseError can be raised in order to
    make the flask application return a certain response
    Usage:
        >>> raise BaseResponseError(
            "something didn't work out",
            status_code=500,
            payload={
                "context": "lib.placeholder.placeholder",
                "critical": False,
            },
            description="Something bad has happened because of ...",
        )
    """
    default_status_code = 400

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        payload: Optional[Mapping] = None,
        description: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code or self.default_status_code
        self.payload = payload
        self.description = description

    def to_flask_response(self) -> Response:
        payload = dict(self.payload or (), message=self.message)
        response = jsonify(payload)
        response.status_code = self.status_code
        return response
