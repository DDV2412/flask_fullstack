# auth.py

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from app.utils.login_required import login_required

from app.utils.scrapping_in_review import InReviewScrapping


class Submission:
    def __init__(self, app):
        self.app = app
        with self.app.app_context():
            self.inreview_service = current_app.services['inreview']
        self.blueprint = Blueprint('submission', __name__)

        # Define routes using self.service
        
        @self.blueprint.route('/submission', methods=['GET'])
        @login_required
        def submission():

            submissions = self.inreview_service.get_all_inreviews()

            return render_template('dashboard/in_review/index.html', submissions=submissions)
        

        @self.blueprint.route('/update/submission', methods=['POST'])
        @login_required
        def update_submission():
            success_message = None


            journal_lists = [
                {
                    "url": "https://iaesprime.com/index.php/csit",
                    "journal_name": "Computer Science and Information Technologies",
                    "payload": {"username": "cmedia", "password": "254#@#@778&%"},
                },
                {
                    "url": "https://ijece.iaescore.com/index.php/IJECE",
                    "journal_name": "International Journal of Electrical and Computer Engineering (IJECE)",
                    "payload": {"username": "ijecemedia", "password": "254#@#@778&%"},
                },
                {
                    "url": "https://ijeecs.iaescore.com/index.php/IJEECS",
                    "journal_name": "Indonesian Journal of Electrical Engineering and Computer Science",
                    "payload": {"username": "ijecemedia", "password": "254#@#@778&%$"},
                },
                {
                    "url": "https://ijaas.iaescore.com/index.php/IJAAS",
                    "journal_name": "International Journal of Advances in Applied Sciences",
                    "payload": {"username": "imedia", "password": "254#@#@778&%"},
                },
                {
                    "url": "https://ijict.iaescore.com/index.php/IJICT",
                    "journal_name": "International Journal of Informatics and Communication Technology (IJ-ICT)",
                    "payload": {"username": "imedia", "password": "254#@#@778&%"},
                },
                {
                    "url": "https://ijres.iaescore.com/index.php/IJRES",
                    "journal_name": "International Journal of Reconfigurable and Embedded Systems (IJRES)",
                    "payload": {"username": "imedia", "password": "254#@#@778&%"},
                },
                {
                    "url": "https://ijra.iaescore.com/index.php/IJRA",
                    "journal_name": "IAES International Journal of Robotics and Automation (IJRA)",
                    "payload": {"username": "imedia", "password": "254#@#@778&%"},
                },
                {
                    "url": "https://www.beei.org/index.php/EEI",
                    "journal_name": "Bulletin of Electrical Engineering and Informatics",
                    "payload": {"username": "ijecemedia", "password": "254#@#@778&%$"},
                },
                {
                    "url": "https://ijai.iaescore.com/index.php/IJAI",
                    "journal_name": "IAES International Journal of Artificial Intelligence (IJ-AI)",
                    "payload": {"username": "ddv", "password": "254#@#@778&%"},
                },
                {
                    "url": "https://ijpeds.iaescore.com/index.php/IJPEDS",
                    "journal_name": "International Journal of Power Electronics and Drive Systems (IJPEDS)",
                    "payload": {"username": "ddv", "password": "254#@#@778&%"},
                },
                {
                    "url": "https://ijape.iaescore.com/index.php/IJAPE",
                    "journal_name": "International Journal of Applied Power Engineering (IJAPE)",
                    "payload": {"username": "ijecemedia", "password": "254#@#@778&%$"},
                },
                {
                    "url": "https://ijere.iaescore.com/index.php/IJERE",
                    "journal_name": "International Journal of Evaluation and Research in Education (IJERE)",
                    "payload": {"username": "imedia", "password": "254#@#@778&%"},
                },
                {
                    "url": "https://edulearn.intelektual.org/index.php/EduLearn",
                    "journal_name": "Journal of Education and Learning (EduLearn)",
                    "payload": {"username": "emedia", "password": "254#@#@778&%$"},
                },
                {
                    "url": "http://telkomnika.uad.ac.id/index.php/TELKOMNIKA",
                    "journal_name": "TELKOMNIKA (Telecommunication Computing Electronics and Control)",
                    "payload": {"username": "ijecemedia", "password": "254#@#@778&%$"},
                },
            ]

            for journal in journal_lists:
                scraper = InReviewScrapping(journal)
                scraper_data = scraper.run()

                for submission in scraper_data:
                    self.inreview_service.create_inreview(submission)
                success_message = f"Success {journal['journal_name']}"

                flash(success_message)


            return redirect(url_for('submission.submission'))
        

        @self.blueprint.route('/submission/delete', methods=['POST'])
        @login_required
        def delete_submission():
            success_message = None
            id = request.form.get('submission_id')
            submission = self.inreview_service.find_by_id(id)

            data = {
                    'action' : request.form.get('action'),
                }
                
            try:
                self.inreview_service.update_inreview(submission['_id'],data)
                success_message = f'Submission successfully updated with ID: {id}'

                flash(success_message)

            except Exception as error:
                success_message = f'{str(error)}'
                flash(success_message)

            return redirect(url_for('submission.submission'))

        

       
    


