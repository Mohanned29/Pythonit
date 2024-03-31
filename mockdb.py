from werkzeug.security import generate_password_hash

#mock data simulating the user table in a database


#hashing the passwords :
plaintext_password1 = "mypassword1"
plaintext_password2 = "mypassword2"
plaintext_password3 = "mypassword3"
plaintext_password4 = "mypassword4"
plaintext_password5 = "mypassword5"

hashed_password1 = generate_password_hash(plaintext_password1)
hashed_password2 = generate_password_hash(plaintext_password2)
hashed_password3 = generate_password_hash(plaintext_password3)
hashed_password4 = generate_password_hash(plaintext_password4)
hashed_password5 = generate_password_hash(plaintext_password5)


users = {
    'teacher1': {'username': 'teacher1', 'password': hashed_password1, 'id': 1, 'schedule': []},
    'teacher2': {'username': 'teacher2', 'password': hashed_password2, 'id': 2, 'schedule': []},
    'teacher3': {'username': 'teacher3', 'password': hashed_password3, 'id': 3, 'schedule': []},
    'teacher4': {'username': 'teacher4', 'password': hashed_password4, 'id': 4, 'schedule': []},
    'teacher5': {'username': 'teacher5', 'password': hashed_password5, 'id': 5, 'schedule': []},
}

def add_user(username, password):
    if username in users:
        return False
    user_id = max(users.keys(), default=0) + 1
    users[username] = {
        'username': username,
        'password': generate_password_hash(password),
        'id': user_id,
        'schedule': []
    }
    return True


def get_user_by_username(username):
    return users.get(username)

def get_schedule_by_user_id(user_id):
    return users[user_id]['schedule']
