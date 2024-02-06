from flask import Blueprint, current_app, render_template, request

class Home:
    def __init__(self, app):
        self.app = app
        with self.app.app_context():
            self.service = current_app.services['article']

        self.blueprint = Blueprint('home', __name__)

        # Define routes using self.service
        @self.blueprint.route('/', methods=['GET'])
        def home():
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 15))
            search = request.args.get("search", None)
            sort_field = request.args.get("publish_at", 'desc')
            sort_order = request.args.get("sort_order", None)
            journal_filter = request.args.get("source_title", None)
            author_filter = request.args.get("creator", None)
            singleYear = request.args.get("singleYear", None)
            minYear = request.args.get("minYear", None)
            maxYear = request.args.get("maxYear", None)
            searchWithin = request.args.get("searchWithin", None)
            isFeatured = request.args.get("isFeatured", 'true')
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
            return render_template('frontend/index.html', articles=articles)
    
        
        