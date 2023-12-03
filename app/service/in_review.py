# service.py

class InReviewService:
    def __init__(self, inreview_repository):
        self.inreview_repository = inreview_repository

    def create_inreview(self, inreview):
        # Additional business logic can be added here before calling the repository
        inreview_id = self.user_repository.create_user(inreview)
        return inreview_id

    def get_all_inreviews(self):
        inreviews = self.inreview_repository.get_all_inreviews()
        return inreviews
