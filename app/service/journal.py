# service.py

class JournalService:
    def __init__(self, journal_repository):
        self.journal_repository = journal_repository

    def create_journal(self, journal):
        journal_id = self.journal_repository.create_journal(journal)
        return journal_id
    
    def get_all_journals(self):
        return self.journal_repository.find_all_journals()
    
    def find_by_id(self, journal_id):
        return self.journal_repository.find_by_id(journal_id)
    
    def update_journal(self, journal_id, updates):
        self.journal_repository.update_journal(journal_id, updates)

    def delete_journal(self, journal_id):
        self.journal_repository.delete_journal(journal_id)

