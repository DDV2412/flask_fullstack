from flask import Blueprint, render_template

class Conferences:
    def __init__(self, ):

        self.blueprint = Blueprint('conferences', __name__)

        # Define routes using self.service
        @self.blueprint.route('/conferences', methods=['GET'])
        def conferences():
            return render_template('frontend/conference.html')
    
        
        