class UserModel:
    def __init__(self, fpath):
        self.path = fpath
        self._users = {}  # Initialize the dictionary
        self.__get_all_users__()
        
    def __get_all_users__(self):
        with open(self.path, 'r') as f:
            for line in f:
                user_id, username, age = line.strip().split(",")
                self._users[int(user_id)] = ({"user_id": user_id, "username": username, "age":int(age)})
        self._users = self._users  
        self._next_user_id = max(self._users.keys())+1 
    
    def __persist_users__(self):
        with open(self.path, 'w')as f:
            for u in self._users.values():
                f.write(f"{u['user_id']},{u['username']},{u['age']}\n")
            
    def get_users(self, user_id, items = None, offset = None, filter_by= None):
        if user_id is None:
            items = len(self._users) if items is None else items 
            offset = 0 if offset is None else offset
            users = list(self._users.values())[offset:offset+items]  # Return just one paginate
            return users if filter_by is None else self.filter(users, filter_by)
        elif user_id in self._users:
            return self._users[user_id]
        else:
            return {} 
        
    def filter(self, users, filter_by):
        for op in {">", "=","<"}:
            if op in filter_by:
                #filter_by => age>10
                #age, 10 = field, val
                #user = {"age":10, "username":Andy}
                field, val = filter_by.split(op)
                op = "==" if op is "=" else op
                return [user for user in users if field in user and eval(f"{user[field]}{op}{val}")]
        return []
                

    def new_user(self, username, age):
        with open(self.path, 'a') as f:
            f.write(f"{self._next_user_id},{username},{age}\n")  # Ensure newline is there
        user = {"user_id": self._next_user_id, "username": username, "age":age}
        self._users[self._next_user_id] = user
        self._next_user_id+=1
        return user
        
    def delete_user(self, user_id):
        if user_id in self._users:
            user = self._users.pop(user_id)
            self.__persist_users__() 
            return user
        else:
            return {}
        
    def update_user(self, user_id, username=None, age=None):
        if user_id in self._users:
            user = self._users[user_id]
            if username is not None:
                user["username"] = username
            if age is not None:
                user["age"] = age
            self.__persist_users__() 
            return user
        else:
            return {}
            
            
        
