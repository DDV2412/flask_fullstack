from flask import Blueprint, render_template

class Home:
    def __init__(self):
        self.blueprint = Blueprint('home', __name__)

        # Define routes using self.service
        @self.blueprint.route('/', methods=['GET'])
        def home():
            return render_template('frontend/index.html')
    
        
        