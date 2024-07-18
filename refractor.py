from flask import Flask, jsonify, g
from performance import Performance
from v1 import v1_bp
import uuid, time

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")  # Ensure config module is correctly set up
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

app.register_blueprint(v1_bp,url_prefix="/v1")

if __name__ == '__main__':
    print(app.url_map)
    app.run(port=8001)
    