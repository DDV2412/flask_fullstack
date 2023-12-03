# auth.py

from flask import Blueprint, redirect, render_template, request, url_for


class Dashboard:
    def __init__(self):
        self.blueprint = Blueprint('dashboard', __name__)

        @self.blueprint.route('/dashboard', methods=['GET'])
        def dashboard():

            return render_template('dashboard/index.html')
        
        
    


