# auth.py

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from app.models import User as UserModel
from werkzeug.security import check_password_hash, generate_password_hash

from app.utils.login_required import login_required


class User:
    def __init__(self, app):
        self.app = app
        with self.app.app_context():
            self.user_service = current_app.services['user']
        self.blueprint = Blueprint('user', __name__)

        # Define routes using self.service
        @self.blueprint.route('/user', methods=['GET', 'POST'])
        @login_required
        def user():
            success_message = None

            if request.method == 'POST':
                data = {
                    'name' : request.form.get('name'),
                    'email' : request.form.get('email'),
                    'password': generate_password_hash(request.form.get('password')),
                    'user_role': request.form.get('role')

                }
                
                try:

                    user_dict = UserModel(**data)
                    user_dict.validate()
                    user = self.user_service.create_user(data)
                    success_message = f'User successfully created with ID: {user}'
                    flash(success_message)

                except Exception as error:
                    success_message = f'{str(error)}'
                    flash(success_message)

            users = self.user_service.get_all_users()

            return render_template('dashboard/user/index.html', users=users)
        
        @self.blueprint.route('/user/edit', methods=['POST'])
        @login_required
        def edit_user():
            success_message = None
            if request.method == 'POST':
                user_id = request.form.get("edit_id")
                data = {
                    'name' : request.form.get('name'),
                    'email' : request.form.get('email'),
                    'user_role': request.form.get('role')

                }
                
                try:
                    self.user_service.update_user(user_id, data)

                    success_message = f'User successfully updated with ID: {user_id}'
                    flash(success_message)

                except Exception as error:
                    success_message = f'{str(error)}'
                    flash(success_message)

            return redirect(url_for('user.user'))
    
        @self.blueprint.route('/delete/user', methods=['POST'])
        @login_required
        def delete_user():
            success_message = None

            user_id = request.form.get('delete_id')

            try:
                self.user_service.delete_user(user_id)
                success_message = f'User successfully deleted with ID: {user_id}'

                flash(success_message)
            except Exception as error:
                success_message = f'{str(error)}'

                flash(success_message)

            return redirect(url_for('user.user'))
    


