from flask import Blueprint, render_template

class Blog:
    def __init__(self):
        self.blueprint = Blueprint('blog', __name__)

        # Define routes using self.service
        @self.blueprint.route('/blog', methods=['GET'])
        def blog():
            return render_template('frontend/blog.html')
    
        
        