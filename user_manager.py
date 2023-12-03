# user_manager.py
import json


class UserManager:
    def __init__(self):
        with open('users.json', "r") as f:
            self.users_data = json.load(f)

    # A method that writes a new password to the user data file.
    def write_password(self, username, password):
        self.users_data[username] = password

        with open('users.json', "w") as f:
            json.dump(self.users_data, f, indent=2)

    # A method to verify a password.
    # Returns true if the password for this username is correct
    def verify_password(self, username, password):
        return self.users_data.get(username) == password

