# auth.py

from flask import Blueprint, render_template, current_app

class Article:
    def __init__(self, app):
        self.app = app
        with self.app.app_context():
            self.service = current_app.services['article']
        self.blueprint = Blueprint('article', __name__)

        # Define routes using self.service
        @self.blueprint.route('/article', methods=['GET'])
        def article():
            articles = self.service.get_all_articles()

            return render_template('dashboard/article/index.html', articles=articles)
    
        
        @self.blueprint.route('/article/edit', methods=['GET', 'PATCH'])
        def edit_article():
            article = {}
            return render_template('dashboard/article/edit.html')
    
        
    


