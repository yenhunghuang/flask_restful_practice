from flask_restful import Resource, reqparse, request
from flask import after_this_request
from flask import current_app as app
from performance import Performance

class MessageResources(Resource):
    
    def __init__(self):
        self.queue = []
        self.parser =reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('datadate', type = str, help="datadate must be string", required = True)
        self.parser.add_argument('location', type=str, help="location must be string", required = True)
        
    def post(self, user_id):
        @after_this_request
        def set_cookie(response):
            response.set_cookie("sent messages before", value="true")
            response.set_cookie("message_only", value="1", path = "/message/1")
            return response
        app.logger.info(dict(request.cookies))
        
        token = request.headers.get("token")
        if token is None:
            return None, 401, {"www-authenticate": "A required token must exist"}
        elif not self.token_is_valid(token):
            return None,403
        else:
            args = self.parser.parse_args()
            self.queue.append({
                "user_id": user_id,
                "datadate": args.get("datadate"),
                "llocation": args.get("location") 
            })
            print(self.queue)
            return "Acknoldge", 202
            
    def token_is_valid(self, token):
        return token == "token"
        