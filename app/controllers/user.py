# auth.py

from flask import Blueprint, render_template

from app.utils.scrapping_article import RequestOAI

class User:
    def __init__(self):
        self.blueprint = Blueprint('user', __name__)

        # Define routes using self.service
        @self.blueprint.route('/user', methods=['GET'])
        def user():
            return render_template('dashboard/user/index.html')
    
        
    


