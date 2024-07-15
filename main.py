from flask import Flask, jsonify, request
from users import UserModel  # Make sure the module and class names are correct

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")  # Ensure config module is correctly set up

user_model = UserModel('user.csv')  # Ensure the UserModel class is designed to handle initialization with CSV

@app.route("/users",defaults={"user_id":None}, methods=['GET'])
@app.route("/users/<int:user_id>", methods=['GET'])
def get_users(user_id):
    users = user_model.get_users(user_id)
    return jsonify(users)

@app.route("/users", methods=['POST'])
def new_user():
    user = user_model.new_user(username=request.json["username"], age=request.json["age"])
    response = jsonify(user)
    response.headers["Location"] = f"users/{user['user_id']}"  # Corrected to proper dictionary string access and Location header
    return response

@app.route("/users/<int:user_id>", methods=['Delete'])
def delete_user(user_id):
    user = user_model.delete_user(user_id)
    return jsonify(user)

@app.route("/users/<int:user_id>", methods=['PUT', 'PATCH'])
def update_user(user_id):
    username = request.json["username"] if "username" in request.json else None
    age = request.json["age"] if "age" in request.json else None
    user = user_model.update_user(user_id,username=username,age=age)
    return jsonify(user)
        

if __name__ == '__main__':
    app.run(port=8001)
    