from flask_login import UserMixin
from mockdb import get_user_by_username

class User(UserMixin):
    def __init__(self, username, user_id):
        self.username = username
        self.id = user_id

    @staticmethod
    #load a user from your mock database
    def get(user_id):
        user_data = get_user_by_username(user_id)
        if user_data:
            return User(user_data['username'], user_data['id'])
        return None
