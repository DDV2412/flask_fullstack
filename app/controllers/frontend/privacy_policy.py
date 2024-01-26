from flask import Blueprint, render_template

class Policy:
    def __init__(self):
        self.blueprint = Blueprint('policy', __name__)

        # Define routes using self.service
        @self.blueprint.route('/privacy-policy', methods=['GET'])
        def policy():
            return render_template('frontend/privacy-policy.html')
    
        
        