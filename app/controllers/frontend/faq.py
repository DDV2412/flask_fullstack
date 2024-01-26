from flask import Blueprint, render_template

class Faq:
    def __init__(self):
        self.blueprint = Blueprint('faq', __name__)

        # Define routes using self.service
        @self.blueprint.route('/faqs', methods=['GET'])
        def faq():
            return render_template('frontend/faqs.html')
    
        
        