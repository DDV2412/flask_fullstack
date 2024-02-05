from flask import Blueprint, render_template

class Advanced:
    def __init__(self):
        self.blueprint = Blueprint('advanced', __name__)

        # Define routes using self.service
        @self.blueprint.route('/advanced-search', methods=['GET'])
        def advanced():
            return render_template('frontend/advanced.html')
    
        
        