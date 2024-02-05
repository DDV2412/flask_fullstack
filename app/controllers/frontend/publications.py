from flask import Blueprint, current_app, redirect, render_template, request, url_for

class Publications:
    def __init__(self, app):
        self.app = app
        with self.app.app_context():
            self.journal_service = current_app.services['journal']
        self.blueprint = Blueprint('publications', __name__)

        # Define routes using self.service
        @self.blueprint.route('/publications', methods=['GET'])
        def publications():
            journals = self.journal_service.get_all_journals()

            return render_template('frontend/publications.html', journals=journals)
        

        
        
    
        
        