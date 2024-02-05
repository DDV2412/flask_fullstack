#routers

from app.controllers.article import Article
from app.controllers.auth import Auth
from app.controllers.dashboard import Dashboard
from app.controllers.file_upload import FileController
from app.controllers.frontend.about import About
from app.controllers.frontend.advanced import Advanced
from app.controllers.frontend.articles import Articles
from app.controllers.frontend.blog import Blog
from app.controllers.frontend.conferences import Conferences
from app.controllers.frontend.contact import Contact
from app.controllers.frontend.faq import Faq
from app.controllers.frontend.home import Home
from app.controllers.frontend.privacy_policy import Policy
from app.controllers.frontend.publications import Publications
from app.controllers.frontend.terms import Terms
from app.controllers.journal import Journal
from app.controllers.submission import Submission
from app.controllers.user import User
from app.controllers.frontend.not_found import NotFound


def init_router(app):
    auth_router = Auth(app)
    app.register_blueprint(auth_router.blueprint)

    dashboard_router = Dashboard()
    app.register_blueprint(dashboard_router.blueprint)

    journal_router = Journal(app)
    app.register_blueprint(journal_router.blueprint)

    submission_router = Submission(app)
    app.register_blueprint(submission_router.blueprint)

    article_router = Article(app)
    app.register_blueprint(article_router.blueprint)

    user_router = User(app)
    app.register_blueprint(user_router.blueprint)

    file_router = FileController(app)
    app.register_blueprint(file_router.blueprint)

    index_router = Home()
    app.register_blueprint(index_router.blueprint)

    about_router = About()
    app.register_blueprint(about_router.blueprint)

    notfound_router = NotFound()
    app.register_blueprint(notfound_router.blueprint)

    articles_router = Articles(app)
    app.register_blueprint(articles_router.blueprint)

    blog_router = Blog()
    app.register_blueprint(blog_router.blueprint)

    conferences_router = Conferences()
    app.register_blueprint(conferences_router.blueprint)

    contact_router = Contact()
    app.register_blueprint(contact_router.blueprint)

    faq_router = Faq()
    app.register_blueprint(faq_router.blueprint)

    policy_router = Policy()
    app.register_blueprint(policy_router.blueprint)

    term_router = Terms()
    app.register_blueprint(term_router.blueprint)

    publications_router = Publications(app)
    app.register_blueprint(publications_router.blueprint)

    advanced_router = Advanced()
    app.register_blueprint(advanced_router.blueprint)

    return app
