import json


class AccountHandler:

    # A method to verify a password.
    # Returns true if the password for this username is correct
    def verify_password(self, users_data, username, password):
        return users_data.get(username) == password

    # Returns true if the Admin password is correct
    def verify_admin(self, users_data, username, password):
        return users_data.get("Admin") == password
