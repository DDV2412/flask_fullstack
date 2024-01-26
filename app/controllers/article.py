# auth.py

from flask import Blueprint, flash, redirect, render_template, current_app, request, url_for

from app.utils.login_required import login_required

class Article:
    def __init__(self, app):
        self.app = app
        with self.app.app_context():
            self.service = current_app.services['article']
        self.blueprint = Blueprint('article', __name__)

        # Define routes using self.service
        @self.blueprint.route('/article', methods=['GET'])
        @login_required
        def article():
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 15))
            search = request.args.get("search", None)
            sort_field = request.args.get("sort_field", None)
            sort_order = request.args.get("sort_order", None)
            subject_filter = request.args.get("subject_filter", None)
            journal_filter = request.args.get("journal_filter", None)
            author_filter = request.args.get("author_filter", None)
            singleYear = request.args.get("singleYear", None)
            minYear = request.args.get("minYear", None)
            maxYear = request.args.get("maxYear", None)
            searchWithin = request.args.get("searchWithin", None)
            featured = request.args.get("featured", False)
            advancedQuery = request.args.get("advancedQuery", None)
            articles = self.service.get_all_articles(page,
                per_page,
                search,
                sort_field,
                sort_order,
                subject_filter,
                journal_filter,
                author_filter,
                singleYear,
                minYear,
                maxYear,
                searchWithin,
                featured,
                advancedQuery)

            return render_template('dashboard/article/index.html', articles=articles)
    
        
        @self.blueprint.route('/article/<id>/edit', methods=['GET', 'POST'])
        @login_required
        def edit_article(id):
            article = self.service.find_by_id(id)

            if request.method == 'POST':
                

                
                creators = []
                for key, value in request.form.items():
                    if key.startswith('creators'):
                        index = key.split('[')[1].split(']')[0]
                        if len(creators) <= int(index):
                            creators.append({})
                        field = key.split('[')[2].split(']')[0]
                        creators[int(index)][field] = value

                featured_form_value = request.form.get('featured')

                featured = True if featured_form_value and featured_form_value.lower() == 'on' else False

                
                data = {
                        'title' : request.form.get('title'),
                        'doi' : request.form.get('doi'),
                        'abstract' : request.form.get('abstract'),
                        'thumbnail_image' : request.form.get('thumbnail_image'),
                        'file_view' : request.form.get('file_view'),
                        'content' : request.form.get('content'),
                        'featured' : featured,
                        'creators': creators
                    }
                    
                try:
                    article = self.service.update_article(article['_id'], data)
                    success_message = f'Article successfully updated with ID: {id}'
                    flash(success_message)


                    return redirect(url_for('article.article'))

                except Exception as error:
                    success_message = f'{str(error)}'
                    flash(success_message)
                    
            return render_template('dashboard/article/edit.html', article=article)
        
        @self.blueprint.route('/delete/article', methods=['POST'])
        @login_required
        def delete_article():
            success_message = None

            article_id = request.form.get('delete_id')

            try:
                self.service.delete_article(article_id)
                success_message = f'Article successfully deleted with ID: {article_id}'

                flash(success_message)
            except Exception as error:
                success_message = f'{str(error)}'

                flash(success_message)

            return redirect(url_for('article.article'))
    
        
    


