# auth.py

from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for

from app.utils.scrapping_article import RequestOAI
from app.models import Journal as JournalModel

class Journal:
    def __init__(self, app):
        self.app = app
        with self.app.app_context():
            self.journal_service = current_app.services['journal']
            self.article_service = current_app.services['article']
        self.blueprint = Blueprint('journal', __name__)

        # Define routes using self.service
        
        @self.blueprint.route('/journal', methods=['GET', 'POST'])
        def journal():
            success_message = None

            if request.method == 'POST':
                journal_id = request.form.get()['journal_id']

                try:
                    self.journal_service.delete_journal(journal_id)
                    success_message = f'Journal successfully deleted with ID: {journal_id}'

                    flash(success_message)
                except Exception as error:
                    success_message = f'{str(error)}'

                    flash(success_message)


            journals = self.journal_service.get_all_journals()

            return render_template('dashboard/journal/index.html', journals=journals)
        

        @self.blueprint.route('/journal/sync', methods=['POST'])
        def sync_journal():
            success_message = None
            status_code = 200
            journal_id = request.form.get()['journal_id']
                    
            try:
                journal = self.journal_service.find_by_id(journal_id)

                request_instance = RequestOAI(request)

                results = request_instance.request_oai(
                journal["site_url"], journal["abbreviation"])

                for result in results["results"]:
                    doi = result.get("doi")
                    if doi is None or not doi.strip():
                        continue

                    # Set journal info into each result
                    result["journal"] = journal

                    self.article_service.create_or_update_article(result)

                success_message = f'Request OAI successfully with counts: {len(results["results"])}'
                status_code = 200
            except Exception as error:
                print(f'{str(error)}')
                success_message = f'{str(error)}'
                status_code = 400

                return jsonify({'error_message': success_message}), status_code

            return jsonify({'message': success_message}), status_code
 
        

        @self.blueprint.route('/journal/add', methods=['GET', 'POST'])
        def add_journal():
            success_message = None
            status_code = 200
            
            if request.method == 'POST':
                data = {
                    'title' : request.form.get('title'),
                    'short_summary' : request.form.get('short_summary'),
                    'content': request.form.get('description'),
                    'issn' : request.form.get('issn'),
                    'e_issn' : request.form.get('e-issn'),
                    'abbreviation' : request.form.get('abbreviation'),
                    'site_url' : request.form.get('sites'),
                    'main_image' : request.form.get('main_image'),
                    'thumbnail_image': request.form.get('thumbnail_image'),
                    'contact_detail' : request.form.get('email'),
                    'editor_in_chief' : request.form.get('editor')
                }
                
                try:

                    journal_dict = JournalModel(**data)
                    journal_dict.validate()
                    journal = self.journal_service.create_journal(data)
                    success_message = f'Journal successfully created with ID: {journal}'
                    flash(success_message)

                except Exception as error:
                    success_message = f'{str(error)}'
                    flash(success_message)
            
            return render_template('dashboard/journal/add.html')

        
        @self.blueprint.route('/journal/<id>/edit', methods=['GET', 'POST'])
        def edit_journal(id):
            success_message = None
            journal = self.journal_service.find_by_id(id)

            if request.method == 'POST':
                data = {
                    'title' : request.form.get('title'),
                    'short_summary' : request.form.get('short_summary'),
                    'content': request.form.get('description'),
                    'issn' : request.form.get('issn'),
                    'e_issn' : request.form.get('e-issn'),
                    'abbreviation' : request.form.get('abbreviation'),
                    'site_url' : request.form.get('sites'),
                    'main_image' : request.form.get('main_image'),
                    'thumbnail_image': request.form.get('thumbnail_image'),
                    'contact_detail' : request.form.get('email'),
                    'editor_in_chief' : request.form.get('editor')
                }
                
                try:
                    journal = self.journal_service.update_journal(journal['_id'],data)
                    success_message = f'Journal successfully updated with ID: {id}'

                    flash(success_message)


                    return redirect(url_for('journal.journal'))

                except Exception as error:
                    success_message = f'{str(error)}'
                    flash(success_message)
                    
            return render_template('dashboard/journal/edit.html', journal=journal)

        
    


