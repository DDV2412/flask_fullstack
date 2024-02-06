from flask import Blueprint, render_template, current_app, request

class Articles:
    def __init__(self, app):
        self.app = app
        with self.app.app_context():
            self.service = current_app.services['article']
        self.blueprint = Blueprint('articles', __name__)


        
        # Define routes using self.service
        @self.blueprint.route('/articles', methods=['GET'])
        def articles():
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 15))
            search = request.args.get("search", None)
            sort_field = request.args.get("sort_field", None)
            sort_order = request.args.get("sort_order", None)
            journal_filter = request.args.get("source_title", None)
            author_filter = request.args.get("creator", None)
            singleYear = request.args.get("singleYear", None)
            minYear = request.args.get("minYear", None)
            maxYear = request.args.get("maxYear", None)
            searchWithin = request.args.get("searchWithin", None)
            isFeatured = request.args.get("isFeatured", None)
            advancedQuery = request.args.get("advancedQuery", None)
            articles = self.service.get_all_articles(page,
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
                advancedQuery)
            

            return render_template('frontend/articles.html', articles=articles)
        
        @self.blueprint.route('/article/<id>', methods=['GET'])
        def article_detail(id):
            article = self.service.find_by_id(id)

            return render_template('frontend/article_detail.html', article=article)
        
        
    
        
        