# repository.py

import re
from bson import ObjectId
import pymongo
from app.models import Article

class ArticleRepository:
    def __init__(self, db):
        self.db = db
        self.article_collection = self.db[Article.__name__]

        self.article_collection.create_index(
            [
                ("title", pymongo.TEXT),
                ("description", pymongo.TEXT),
                ("content", pymongo.TEXT),
                ("creators", pymongo.TEXT),
                ("subjects", pymongo.TEXT),
                ("publisher", pymongo.TEXT),
            ]
        )

    def create_article(self, article):
        result = self.article_collection.insert_one(article)
        return result.inserted_id
    

    def find_all_articles(self,
        page=1,
        per_page=15,
        search=None,
        sort_field=None,
        sort_order=None,
        journal_filter=None,
        author_filter=None,
        singleYear=None,
        minYear=None,
        maxYear=None,
        searchWithin=None,
        featured=False,
        advancedQuery=None,):
        
        offset = (page - 1) * per_page

        search_criteria = {}
        sort_criteria = []

        if search:
            regex_search = re.compile(fr'\b{re.escape(search)}\b', re.IGNORECASE)
            search_criteria = {
                "title": {"$regex": regex_search}
            }


        if featured is not None:
            search_criteria["featured"] = featured

        if advancedQuery:
            pattern = r'\(\s*"(?P<field>[^"]+)":\s*(?P<value>[^)]+)\s*\)(?=\s*(?P<operator>[A-Z]+)\s*|\s*$)'

            queries = re.findall(pattern, advancedQuery)

            search_criteria = {"featured": False, "$and": []}

            operator = "AND"

            for token in queries:
                field, value, query_operator = token

                field = field.strip()
                value = value.strip()


                if not query_operator:
                    query_operator = operator

                query = {}

                regex_value = re.compile(fr'\b{re.escape(value)}\b', re.IGNORECASE)

                if operator != "NOT":
                    if field == "All Metadata":
                        query["$" + operator.lower()] = [
                            {"title": {"$regex": regex_value}},
                            {"description": {"$regex": regex_value}},
                            {"subjects": {"$elemMatch": {"$regex": regex_value}}},
                        ]
                    elif field == "Full Text":
                        query["$" + operator.lower()] = [{"$text": {"$search": value}}]
                    elif field == "Document Title":
                        query["$" + operator.lower()] = [{"title": {"$regex": regex_value}}]
                    elif field == "Source Title":
                        query["$" + operator.lower()] = [
                            {"journal.title": {"$regex": regex_value}},
                            {"journal.abbreviation": {"$regex": regex_value}},
                        ]
                    elif field == "Authors":
                        query["$" + operator.lower()] = [
                            {"creators": {"$elemMatch": {'name': {"$regex": regex_value}}}}
                        ]
                    elif field == "Abstract":
                        query["$" + operator.lower()] = [
                            {"description": {"$regex": regex_value}}
                        ]
                    elif field == "DOI":
                        query["$" + operator.lower()] = [{"doi": {"$regex": regex_value}}]
                    elif field == "Issue":
                        query["$" + operator.lower()] = [{"issue": {"$regex": regex_value}}]
                    elif field == "Article Page Number":
                        query["$" + operator.lower()] = [{"pages": {"$regex": regex_value}}]
                    elif field == "Keywords":
                        query["$" + operator.lower()] = [
                            {"subjects": {"$elemMatch": {"$regex": regex_value}}}
                        ]
                else:
                    if field == "All Metadata":
                        query["$nor"] = [
                            {"title": {"$regex": regex_value}},
                            {"description": {"$regex": regex_value}},
                        ]
                    elif field == "Full Text":
                        query["$nor"] = [
                            {"$text": {"$search": regex_value}},
                        ]
                    elif field == "Document Title":
                        query["$nor"] = [
                            {"title": {"$regex": regex_value}},
                        ]
                    elif field == "Source Title":
                        query["$nor"] = [
                            {"journal.title": {"$regex": regex_value}},
                            {"journal.abbreviation": {"$regex": regex_value}},
                        ]
                    elif field == "Authors":
                        query["$nor"] = [
                            {"creators": {"$elemMatch": {'name': {"$regex": regex_value}}}},
                        ]
                    elif field == "Abstract":
                        query["$nor"] = [
                            {"description": {"$regex": regex_value}},
                        ]
                    elif field == "DOI":
                        query["$nor"] = [
                            {"doi": {"$regex": regex_value}},
                        ]
                    elif field == "Issue":
                        query["$nor"] = [
                            {"issue": {"$regex": regex_value}},
                        ]
                    elif field == "Article Page Number":
                        query["$nor"] = [
                            {"pages": {"$regex": regex_value}},
                        ]
                    elif field == "Keywords":
                        query["$nor"] = [
                            {"subjects": {"$elemMatch": {"$regex": regex_value}}},
                        ]

                search_criteria["$and"].append(query)


        
        if sort_field and sort_order:
            if sort_field == "relevance":
                sort_criteria.append(("relevance_score", pymongo.DESCENDING))
            else:
                sort_criteria.append(
                    (
                        sort_field,
                        pymongo.ASCENDING
                        if sort_order == "asc"
                        else pymongo.DESCENDING,
                    )
                )
        else:
            sort_criteria.append(("publish_at", pymongo.DESCENDING))


        query = {}
        if search_criteria:
            query.update(search_criteria)

        if journal_filter:
            if not isinstance(journal_filter, list):
                journal_filter = [journal_filter]
            query["journal.title"] = {"$in": journal_filter}

        if author_filter:
            if not isinstance(author_filter, list):
                author_filter = [author_filter]
            query["creators"] = {"$elemMatch": {"name": {"$in": author_filter}}}


        if singleYear:
            query["publish_year"] = singleYear
        elif minYear or maxYear:
            year_filter = {}
            if minYear:
                year_filter["$gte"] = minYear
            if maxYear:
                year_filter["$lte"] = maxYear
            query["publish_year"] = year_filter

        if searchWithin:
            escaped_searchWithin = re.escape(searchWithin)
            search_within_criteria = {
                "$or": [
                    {"title": {"$regex": fr'\b{escaped_searchWithin}\b', "$options": "i"}},
                    {"description": {"$regex": fr'\b{escaped_searchWithin}\b', "$options": "i"}},
                    {"creators.name": {"$regex": fr'\b{escaped_searchWithin}\b', "$options": "i"}},
                ]
            }

            if "$and" not in search_criteria:
                search_criteria["$and"] = []

            if "$text" in search_criteria:
                search_criteria["$and"].append({"$text": search_criteria["$text"]})

            if "$and" in search_criteria:
                search_criteria["$and"].extend(search_criteria.get("$and", []))

            search_criteria["$and"].append(search_within_criteria)

        pipeline = [
            {"$match": query}, 
            {"$facet": {
                "aggr_year": [
                    {"$group": {"_id": "$publish_year", "count": {"$sum": 1}}},
                    {"$match": {"count": {"$gt": 1}}},
                ],
                "aggr_journal": [
                    {"$group": {"_id": "$journal.title", "count": {"$sum": 1}}},
                    {"$match": {"count": {"$gt": 1}}},
                ],
                "aggr_creators": [
                    {"$unwind": "$creators"},
                    {"$group": {"_id": "$creators", "count": {"$sum": 1}}},
                    {"$match": {"count": {"$gt": 1}}},
                ]
            }}
        ]

        aggregated_results = list(self.article_collection.aggregate(pipeline))

        aggr_year = aggregated_results[0]['aggr_year']
        aggr_journal = aggregated_results[0]['aggr_journal']
        aggr_creators = aggregated_results[0]['aggr_creators']

        articles = list(
            self.article_collection.find(query).skip(offset).limit(per_page).sort(sort_criteria)
        )

        for article in articles:
            article["_id"] = str(article["_id"])

        total_articles = self.article_collection.count_documents(query)

        total_pages = (total_articles + per_page - 1) // per_page

        return {
            "articles": articles,
            "aggrs": {
                "years": list(aggr_year),
                "journal": list(aggr_journal),
                "creators": list(aggr_creators),
            },
            "total": total_articles,
            "current_page": page,
            "total_pages": total_pages,
        }
    
    def find_by_id(self, article_id):
        return self.article_collection.find_one({"_id": ObjectId(article_id)})
    
    def find_by_doi(self, doi):
        return self.article_collection.find_one({"doi": doi})
    
    def update_article(self, article_id, updates):
        return self.article_collection.update_one({"_id": ObjectId(article_id)}, {"$set": updates})

    def delete_article(self, article_id):
        return self.article_collection.delete_one({"_id": ObjectId(article_id)})