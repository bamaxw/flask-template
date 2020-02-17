from flask import Blueprint

from . import routes

v1_controller = Blueprint("v1", __name__)

routes.register_routes(v1_controller)
