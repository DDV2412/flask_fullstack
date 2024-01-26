from flask import Blueprint, render_template

class NotFound:
    def __init__(self):
        self.blueprint = Blueprint('notfound', __name__)

        # Define routes using self.service
        @self.blueprint.route('/404', methods=['GET'])
        def notfound():
            return render_template('frontend/404.html')
    
        
        