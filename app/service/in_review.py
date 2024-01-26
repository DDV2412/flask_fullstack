# service.py

class InReviewService:
    def __init__(self, inreview_repository):
        self.inreview_repository = inreview_repository

    def create_inreview(self, inreview):
        journal_name = inreview.get("journal_name")
        submission_id = inreview.get("submission_id")
        existing_submission = self.inreview_repository.find_by_submission_id(submission_id)

        if existing_submission:
            if existing_submission["journal_name"] == journal_name:
                return
        else:
            try:
                return self.inreview_repository.create_inreview(inreview)
            except Exception as e:
                return

    def get_all_inreviews(self):
        inreviews = self.inreview_repository.get_all_inreviews()
        return inreviews
    
    def find_by_id(self, submission_id):
        return self.inreview_repository.find_by_id(submission_id)
    
    def update_inreview(self, submission_id, updates):
        return self.inreview_repository.update_inreview(submission_id, updates)
