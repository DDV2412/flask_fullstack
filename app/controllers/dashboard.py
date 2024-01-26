# auth.py

from flask import Blueprint, g, redirect, render_template, request, url_for

from app.utils.login_required import login_required


class Dashboard:
    def __init__(self):
        self.blueprint = Blueprint('dashboard', __name__)

        @self.blueprint.route('/dashboard', methods=['GET'])
        @login_required
        def dashboard():
            user_log = g.user

            return render_template('dashboard/index.html', user = user_log)
        
        
    


