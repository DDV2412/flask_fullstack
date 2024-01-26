from flask import Blueprint, render_template

class Terms:
    def __init__(self):
        self.blueprint = Blueprint('terms', __name__)

        # Define routes using self.service
        @self.blueprint.route('/terms-and-conditions', methods=['GET'])
        def terms():
            return render_template('frontend/terms-and-conditions.html')
    
        
        