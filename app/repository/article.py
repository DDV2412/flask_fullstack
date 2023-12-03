# repository.py

from bson import ObjectId
from app.models import Article

class ArticleRepository:
    def __init__(self, db):
        self.db = db
        self.article_collection = db[Article.__name__]

    def create_article(self, article):
        result = self.article_collection.insert_one(article)
        return result.inserted_id
    

    def find_all_articles(self):
        articles = list(self.article_collection.find({}))

        for article in articles:
            article["_id"] = str(article["_id"])

        return articles

    def find_by_id(self, article_id):
        return self.article_collection.find_one({"_id": ObjectId(article_id)})
    
    def find_by_doi(self, doi):
        return self.article_collection.find_one({"doi": doi})
    
    def update_article(self, article_id, updates):
        self.article_collection.update_one({"_id": ObjectId(article_id)}, {"$set": updates})

    def delete_article(self, article_id):
        self.article_collection.delete_one({"_id": ObjectId(article_id)})