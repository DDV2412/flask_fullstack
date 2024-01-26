
from bson import ObjectId

from app.models import User


class UserRepository:
    def __init__(self, db):
        self.db = db
        self.user_collection = self.db[User.__name__]
            

    def create_user(self, user):
        result = self.user_collection.insert_one(user)
        return result.inserted_id
    

    def get_all_users(self):
        users = self.user_collection.find().limit(15)

        return users

    def find_by_id(self, user_id):
        return self.user_collection.find_one({"_id": ObjectId(user_id)})
    
    def find_by_email(self, email):
        return self.user_collection.find_one({"email": email})
    
    
    def update_user(self, user_id, updates):
        return self.user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updates})

    def delete_user(self, user_id):
        return self.user_collection.delete_one({"_id": ObjectId(user_id)})