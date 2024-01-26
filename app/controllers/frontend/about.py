from flask import Blueprint, render_template

class About:
    def __init__(self):
  
        self.blueprint = Blueprint('about', __name__)

        # Define routes using self.service
        @self.blueprint.route('/about', methods=['GET'])
        def about():
            return render_template('frontend/about.html')
    
        
        