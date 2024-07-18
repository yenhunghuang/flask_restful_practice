from flask_restful import Resource, fields, marshal_with
from .userResources import user_model, UserResources

class ClassSizeField(fields.Raw):
    def format(self, users):
        return len(users)

class ClassroomResources(Resource):
    class_fields={
        "class_id":fields.Integer(default=-1),
        "class_name":fields.String(default=""),
        "class_size":ClassSizeField(attribute= "students"),
        "students":fields.List(fields.Nested(UserResources.resource_fields), default=[])
    }
    
    def __init__(self):
        self.rooms={
            0:{
                "class_id": 0,
                "class_name": "class_a",
                "students": [0, 1]
            },
            1:{
                "class_id": 1,
                "class_name": "class_b",
                "students": [1, 3, 4]
            }
        }
              
    @marshal_with(class_fields)
    def get(self, class_id=None):
        if class_id is None:
            return [self.update_room_user_info(room) for room in self.rooms.values()]
        elif class_id in self.rooms:
            return self.update_room_user_info(self.rooms[class_id])
        else:
            return {}
        
    def update_room_user_info(self, room):
        room = room.copy()
        room["students"] = list(map(self.update_user_info, room["students"]))
        return room
    def update_user_info(self, user_id):
        return user_model.get_users(user_id)
    
    