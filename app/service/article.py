# service.py

class ArticleService:
    def __init__(self, article_repository):
        self.article_repository = article_repository

    def create_article(self, article):
        article_id = self.article_repository.create_article(article)
        return article_id
    
    def get_all_articles(self,
        page,
        per_page,
        search,
        sort_field,
        sort_order,
        journal_filter,
        author_filter,
        singleYear,
        minYear,
        maxYear,
        searchWithin,
        isFeatured,
        advancedQuery,):
        return self.article_repository.find_all_articles(page,
            per_page,
            search,
            sort_field,
            sort_order,
            journal_filter,
            author_filter,
            singleYear,
            minYear,
            maxYear,
            searchWithin,
            isFeatured,
            advancedQuery,)
    
    def find_by_id(self, article_id):
        return self.article_repository.find_by_id(article_id)
    
    def update_article(self, article_id, updates):
        return self.article_repository.update_article(article_id, updates)

    def delete_article(self, article_id):
        return self.article_repository.delete_article(article_id)

    def create_or_update_article(self, article):
        doi = article.get("doi")
        if doi is None or not doi.strip():
            return

        last_update = article.get("last_update")
        existing_article = self.article_repository.find_by_doi(doi)

        if existing_article:
            if existing_article["last_update"] == last_update:
                return
            else:
                try:
                    self.article_repository.update_article(
                        existing_article["article_id"], article
                    )
                    return
                except Exception as e:
                    return
        else:
            try:
                self.article_repository.create_article(article)
                return
            except Exception as e:
                return

