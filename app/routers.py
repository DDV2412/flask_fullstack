#routers

from app.controllers.article import Article
from app.controllers.auth import Auth
from app.controllers.dashboard import Dashboard
from app.controllers.file_upload import FileController
from app.controllers.journal import Journal
from app.controllers.user import User


def init_router(app):
    auth_router = Auth()
    app.register_blueprint(auth_router.blueprint)

    dashboard_router = Dashboard()
    app.register_blueprint(dashboard_router.blueprint)

    journal_router = Journal(app)
    app.register_blueprint(journal_router.blueprint)

    article_router = Article(app)
    app.register_blueprint(article_router.blueprint)

    user_router = User()
    app.register_blueprint(user_router.blueprint)

    file_router = FileController(app)
    app.register_blueprint(file_router.blueprint)

    return app
