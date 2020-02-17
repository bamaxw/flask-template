import gevent.monkey  # isort:skip

gevent.monkey.patch_all()  # noqa

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS

from superflask.error_handlers import error_handlers


def init_superflask_app(app: Flask) -> Flask:
    """Initialize application with tracing/metrics/healthcheck/sentry etc."""
    app.register_blueprint(error_handlers)

    app.config["SWAGGER"] = {
        "title": app.service_name,
        "uiversion": 3,
        "version": "v1",
    }

    SWAGGER_CFG = {
        "headers": [],
        "specs": [
            {
                "endpoint": "openapi",
                "route": "/openapi.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": f"/{app.service_name}/v1/docs/",
    }

    Swagger(app, config=SWAGGER_CFG)
    CORS(app)
    return app
