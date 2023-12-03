# auth.py

from flask import Blueprint, render_template
from werkzeug.security import check_password_hash, generate_password_hash


class Auth:
    def __init__(self):
        self.blueprint = Blueprint('auth', __name__)

        # Define routes using self.service

        @self.blueprint.route('/login', methods=['POST', 'GET'])
        def login():
            return render_template('auth/login.html')
        

        @self.blueprint.route('/sign-up', methods=['POST', 'GET'])
        def register():
            return render_template('auth/register.html')


