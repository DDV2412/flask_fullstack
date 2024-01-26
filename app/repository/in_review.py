# repository.py

from bson import ObjectId
from app.models import Submission


class InReviewRepository:
    def __init__(self,db):
        self.db = db
        self.inreview_collection = self.db[Submission.__name__]

    def create_inreview(self, inreview):
        result = self.inreview_collection.insert_one(inreview)
        return result.inserted_id

    def get_all_inreviews(self):
        inreviews = self.inreview_collection.find().limit(15)
        return inreviews
    
    def find_by_id(self, submission_id):
        return self.inreview_collection.find_one({"_id": ObjectId(submission_id)})
    
    def find_by_submission_id(self, submission_id):
        return self.inreview_collection.find_one({"submission_id": submission_id})
    

    def update_inreview(self, submission_id, updates):
        return self.inreview_collection.update_one({"_id": ObjectId(submission_id)}, {"$set": updates})

