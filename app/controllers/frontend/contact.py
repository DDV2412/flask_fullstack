from flask import Blueprint, render_template

class Contact:
    def __init__(self):

        self.blueprint = Blueprint('contact', __name__)

        # Define routes using self.service
        @self.blueprint.route('/contact', methods=['GET'])
        def contact():
            return render_template('frontend/contact.html')
    
        
        