# repository.py

import random
from bson import ObjectId

from app.models import Journal


class JournalRepository:
    def __init__(self, db):
        self.db = db
        self.journal_collection = self.db[Journal.__name__]
            

    def create_journal(self, journal):
        result = self.journal_collection.insert_one(journal)
        return result.inserted_id
    

    def find_all_journals(self):
        journals = list(self.journal_collection.find({}))

        random.shuffle(journals)

        return journals

    def find_by_id(self, journal_id):
        return self.journal_collection.find_one({"_id": ObjectId(journal_id)})
    
    def find_by_issn(self, issn):
        return self.journal_collection.find_one({"issn": issn})
    
    def find_by_eissn(self, eissn):
        return self.journal_collection.find_one({"e_issn": eissn})
    
    def find_by_site(self, site):
        return self.journal_collection.find_one({"site_url": site})
    
    def update_journal(self, journal_id, updates):
        self.journal_collection.update_one({"_id": ObjectId(journal_id)}, {"$set": updates})

    def delete_journal(self, journal_id):
        self.journal_collection.delete_one({"_id": ObjectId(journal_id)})