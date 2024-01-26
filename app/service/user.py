# service.py

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, user):
        user_id = self.user_repository.create_user(user)
        return user_id
    
    def get_all_users(self):
        return self.user_repository.get_all_users()
    
    def find_by_id(self, user_id):
        return self.user_repository.find_by_id(user_id)
    
    def find_by_email(self, email):
        return self.user_repository.find_by_email(email)
    
    def update_user(self, user_id, updates):
        return self.user_repository.update_user(user_id, updates)

    def delete_user(self, user_id):
        return self.user_repository.delete_user(user_id)

