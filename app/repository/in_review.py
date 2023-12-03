# repository.py

from app.models import Submission


class InReviewRepository:
    def __init__(self, db):
        self.db = db
        self.inreview_collection = db[Submission.__name__]

    def create_inreview(self, inreview):
        result = self.inreview_collection.insert_one(inreview)
        return result.inserted_id

    def get_all_inreviews(self):
        inreviews = self.inreview_collection.find()
        return list(inreviews)
