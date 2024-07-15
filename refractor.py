from flask import Flask, jsonify, request, g
from flask_restful import Api
from userResources import UserResources
from classroomResources import ClassroomResources
from messageResources import MessageResources
from performance import Performance
import uuid, time

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")  # Ensure config module is correctly set up
api = Api(app)
performance = Performance("performance.csv") #紀錄每一筆response info 到performance.csv

@app.before_request
def preprocess():
    g.uuid = uuid.uuid4()
    g.conn = {"is_connected": True}
    g.start = time.time()
    
@app.after_request
def postprocess(response):
    g.conn = {"is_connected": False}
    g.end = time.time()
    g.status_code = response.status_code
    performance.log(g)
    return response

api.add_resource(UserResources, "/users", "/users/<int:user_id>")
api.add_resource(ClassroomResources, "/classrooms", "/classrooms/<int:class_id>")
api.add_resource(MessageResources, "/message/<int:user_id>")

if __name__ == '__main__':
    app.run(port=8001)
    