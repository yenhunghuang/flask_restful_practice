from flask import Blueprint
from flask_restful import Api
from .userResources import UserResources
# from .classroomResources import ClassroomResources
# from .messageResources import MessageResources

v2_bp = Blueprint("v2_blueprint",__name__)
api = Api(v2_bp)

api.add_resource(UserResources, "/users", "/users/<int:user_id>")