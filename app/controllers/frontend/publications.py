from flask import Blueprint, current_app, render_template

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
        
        @self.blueprint.route('/publication/<id>', methods=['GET'])
        def publication_detail(id):
            journal = self.journal_service.find_by_id(id)

            return render_template('frontend/publication_detail.html', journal=journal)
    
        
        