import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask, current_app
from pymongo import MongoClient

from app.repository.article import ArticleRepository
from app.repository.in_review import InReviewRepository
from app.repository.journal import JournalRepository
from app.routers import init_router
from app.service.article import ArticleService
from app.service.in_review import InReviewService
from app.service.journal import JournalService
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['MONGODB_URI'] = os.getenv("MONGODB_URI")

    app.secret_key = os.getenv("SECRET")


    try:
        client = MongoClient(app.config['MONGODB_URI'])

        db = client.get_database()
        app.logger.info("Connected to the database successfully.")
    except Exception as e:
        app.logger.error(f"Error connecting to the database: {e}")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.database = db

    # Initialize repositories
    inreview_repository = InReviewRepository(db)
    journal_repository = JournalRepository(db)
    article_repository = ArticleRepository(db)

    # Initialize services
    inreview_service = InReviewService(inreview_repository)
    journal_service = JournalService(journal_repository)
    article_service = ArticleService(article_repository)

    # Register services with the current app context
    with app.app_context():
        current_app.services = {
            'inreview': inreview_service,
            'journal': journal_service,
            'article': article_service,
        }

    # Initialize routers
    init_router(app)

    # Configure logging
    configure_logging(app)

    return app

def configure_logging(app):
    try:
        # Setting level untuk logger
        app.logger.setLevel(logging.DEBUG)

        # Membuat formatter untuk log
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] - %(message)s'
        )

        # Menambahkan handler ke logger
        file_handler = RotatingFileHandler(os.path.join(app.instance_path, 'app.log'), maxBytes=10240, backupCount=5)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)
    except Exception as e:
        print(f"Error configuring logging: {e}")
