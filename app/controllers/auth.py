# auth.py

import functools
from flask import Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User as UserModel, UserRole


class Auth:
    def __init__(self, app):
        self.app = app
        with self.app.app_context():
            self.user_service = current_app.services['user']
        self.blueprint = Blueprint('auth', __name__)

        # Define routes using self.service

        @self.blueprint.before_app_request
        def load_logged_in_user():
            user_id = session.get('user_id')

            if user_id is None:
                g.user = None
            else:
                user = self.user_service.find_by_id(user_id)

                if user:
                    g.user = {
                    '_id': user['_id'],
                    'name': user['name'],
                    'email': user['email'],
                    'user_role': user['user_role']
                }
                else:
                    g.user = None
                



        @self.blueprint.route('/login', methods=['POST', 'GET'])
        def login():
            success_message = None
            if request.method == 'POST':
                data = {
                    'email' : request.form.get('email'),
                    'password': request.form.get('password'),
                }
                
                try:                    
                    user = self.user_service.find_by_email(data['email'])

                    if user is None:
                        success_message = f'Invalid Email or Password'
                        flash(success_message)
                    elif not check_password_hash(user['password'], data['password']):
                        success_message = f'Invalid Email or Password'
                        flash(success_message)
                    
                    if success_message is None:
                        user_id_str = str(user['_id'])
                        session['user_id'] = user_id_str
                        return redirect(url_for('dashboard.dashboard'))


                except Exception as error:
                    success_message = f'{str(error)}'
                    flash(success_message)
            return render_template('auth/login.html')
        

        @self.blueprint.route('/sign-up', methods=['POST', 'GET'])
        def register():
            success_message = None
            if request.method == 'POST':
                if(request.form.get('password') != request.form.get('confirmPassword')):
                    success_message = f'Passwords do not match.'
                    flash(success_message)

                data = {
                    'name' : request.form.get('name'),
                    'email' : request.form.get('email'),
                    'password': generate_password_hash(request.form.get('password')),
                    'user_role' : UserRole.READER.value
                }
                
                try:                    
                    user_dict = UserModel(**data)
                    user_dict.validate()
                    self.user_service.create_user(data)
                    return redirect(url_for('auth.login'))


                except Exception as error:
                    success_message = f'{str(error)}'
                    flash(success_message)
 

            return render_template('auth/register.html')
        

        @self.blueprint.route('/logout', methods=['GET'])
        def logout():
            session.clear()
            return redirect(url_for('auth.login'))


