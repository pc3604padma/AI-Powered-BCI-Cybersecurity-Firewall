import bcrypt
from database import users_collection

def create_user(email, password):

    existing = users_collection.find_one({"email": email})

    if existing:
        return False

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users_collection.insert_one({
        "email": email,
        "password": hashed_pw
    })

    return True


def login_user(email, password):

    user = users_collection.find_one({"email": email})

    if not user:
        return False

    if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return True

    return False