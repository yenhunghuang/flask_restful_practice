from flask_restful import Resource, reqparse, marshal_with, fields
from users import UserModel  # Make sure the module and class names are correct
from flask import current_app as app
from flask import g,request
user_model = UserModel('user.csv')  # Ensure the UserModel class is designed to handle initialization with CSV

class UserResources(Resource):
    resource_fields = {
        'user_id': fields.Integer,
        'username': fields.String,
        'age': fields.Integer
    }
    
    def __init__(self):
        self.parser =reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('username', type = str, help="username must be string")
        self.parser.add_argument('age', type=int, help="age must be integer")
    
    @marshal_with(resource_fields)
    def get(self, user_id=None):
        sent_message_before = request.cookies.get("sent messages before")
        if sent_message_before == "true":
            app.logger.info(f"This user-{g.uuid} sent messages before")
        else:
            app.logger.info(f"This user-{g.uuid} has no sent any messages")
        app.logger.info(f"uuid: {g.uuid} is_connected: {g.conn['is_connected']}")
        return user_model.get_users(user_id)
    
    @marshal_with(resource_fields) 
    def post(self):
        parser = self.parser
        parser.add_argument('username', type = str, help="username must be string and required", required = True)
        parser.add_argument('age', type=int, help="age must be integer and required", required = True) 
        args = parser.parse_args()
        user = user_model.new_user(username=args["username"], age=args["age"])
        return user, 201, {'Location': f"/users/{user['user_id']}"} #provides the correct status code

    @marshal_with(resource_fields)
    def delete(self, user_id):
        user = user_model.delete_user(user_id)
        return user
    
    @marshal_with(resource_fields)
    def put(self, user_id):
        return self.update_user(user_id)
    
    @marshal_with(resource_fields)
    def patch(self, user_id):
        return self.update_user(user_id)
    
    def update_user(self,user_id):
        args = self.parser.parse_args()
        user = user_model.update_user(user_id,username=args.get("username"),age=args.get("age"))
        return user