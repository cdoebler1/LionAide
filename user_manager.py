# user_manager.py
import json


class UserManager:
    def __init__(self):
        with open('users.json', "r") as f:
            self.users_data = json.load(f)
