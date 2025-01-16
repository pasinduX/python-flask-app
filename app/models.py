from app import db

def get_user_collection():
    return db["users"]