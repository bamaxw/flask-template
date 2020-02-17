import os
from superflask import route_factory, swagger_factory

thispath = os.path.dirname(os.path.realpath(__file__))

routes, route = route_factory()
swag_from = swagger_factory(f"{thispath}/swagger")
