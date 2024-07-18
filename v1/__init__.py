from flask import Blueprint
from flask_restful import Api
from .userResources import UserResources
from .classroomResources import ClassroomResources
from .messageResources import MessageResources

v1_bp = Blueprint("v1_blueprint",__name__)
api = Api(v1_bp)

api.add_resource(UserResources, "/users", "/users/<int:user_id>")
api.add_resource(ClassroomResources, "/classrooms", "/classrooms/<int:class_id>")
api.add_resource(MessageResources, "/message/<int:user_id>")