from datetime import datetime
from enum import Enum
from flask import current_app
from jsonschema import ValidationError
from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    ReferenceField,
    ListField,
    BooleanField,
    EmbeddedDocument,
    EnumField, EmailField, EmbeddedDocumentField, DoesNotExist
)



class Creator(EmbeddedDocument):
    name = StringField(max_length=90, required=True)
    orcid = StringField(max_length=48)

class Journal(Document):
    title = StringField(max_length=255, required=True)
    short_summary = StringField()
    issn = StringField(max_length=10, required=True, unique=True)
    e_issn = StringField(max_length=10, required=True, unique=True)
    abbreviation = StringField(max_length=10, required=True)
    site_url = StringField(required=True, unique=True)
    content = StringField(default=None)
    thumbnail_image = StringField(default=None)
    main_image = StringField(default=None)
    contact_detail = StringField(required=True)
    editor_in_chief = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def validate(self, clean=True):
        from app.repository.journal import JournalRepository
        journal_repo = JournalRepository(current_app.database)
        self.data = journal_repo
        super(Journal, self).validate(clean)

        required_fields = ['title', 'issn', 'e_issn', 'abbreviation', 'site_url', 'contact_detail', 'editor_in_chief']
        for field in required_fields:
            value = getattr(self, field, None)
            if not value:
                raise ValidationError(f"The {field.replace('_', ' ')} field is mandatory.")
            
        try:
            journal_issn = self.data.find_by_issn(self.issn)
            if(journal_issn):
                raise ValidationError("The ISSN must be unique.")
        except DoesNotExist:
            pass

        try:
            journal_eissn = self.data.find_by_eissn(self.e_issn)
            if(journal_eissn):
                raise ValidationError("The E-ISSN must be unique.")
        except DoesNotExist:
            pass

        try:
            journal_site = self.data.find_by_site(self.site_url)
            if(journal_site):
                raise ValidationError("The SITE URL must be unique.")
        except DoesNotExist:
            pass

        
        length_validations = {'title': 255, 'issn': 10, 'e_issn': 10, 'abbreviation': 10}

        for field, max_length in length_validations.items():
            value = getattr(self, field, None)
            if max_length is not None and value and len(value) > max_length:
                raise ValidationError(f"The {field.replace('_', ' ')} field must not exceed {max_length} characters.")
            
            min_length = getattr(self, f"min_{field}", None)
            if min_length is not None and value and len(value) < min_length:
                raise ValidationError(f"The {field.replace('_', ' ')} field must be at least {min_length} characters.")
        


class Article(Document):
    article_id = StringField(max_length=10, required=True)
    last_update = DateTimeField(default=datetime.utcnow)
    title = StringField(max_length=255, required=True)
    description = StringField()
    content = StringField()
    creators = ListField(EmbeddedDocumentField(Creator))
    subjects = ListField(StringField())
    publisher = StringField()
    publish_at = StringField()
    publish_year = StringField()
    doi = StringField(required=True, unique=True)
    thumbnail_image = StringField()
    main_image = StringField()
    isFeatured = BooleanField(default='false')
    file_view = StringField()
    journal = ReferenceField(Journal)
    volume = StringField()
    issue = StringField()
    pages = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def validate(self, clean=True):
        from app.repository.article import ArticleRepository
        article_repo = ArticleRepository(current_app.database)
        self.data = article_repo
        super(Article, self).validate(clean)

        required_fields = ['title', 'article_id', 'doi']
        for field in required_fields:
            value = getattr(self, field, None)
            if not value:
                raise ValidationError(f"The {field.replace('_', ' ')} field is mandatory.")
            
        try:
            article_doi = self.data.find_by_doi(self.doi)
            if(article_doi):
                raise ValidationError("The DOI must be unique.")
        except DoesNotExist:
            pass
        
        length_validations = {'title': 255, 'article_id': 10}

        for field, max_length in length_validations.items():
            value = getattr(self, field, None)
            if max_length is not None and value and len(value) > max_length:
                raise ValidationError(f"The {field.replace('_', ' ')} field must not exceed {max_length} characters.")
            
            min_length = getattr(self, f"min_{field}", None)
            if min_length is not None and value and len(value) < min_length:
                raise ValidationError(f"The {field.replace('_', ' ')} field must be at least {min_length} characters.")


class SubmissionActionEnum(Enum):
    INREVIEW = 'inreview'
    DECLINE = 'decline'
    REJECT = 'reject'

class Submission(Document):
    submission_id = StringField(max_length=10, required=True)
    title = StringField(max_length=255, required=True)
    journal_name = StringField()
    authors = StringField()
    action = EnumField(SubmissionActionEnum, default=SubmissionActionEnum.INREVIEW)
    date_submitted = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def validate(self, clean=True):
        from app.repository.in_review import InReviewRepository
        in_review = InReviewRepository(current_app.database)
        self.data = in_review
        super(Submission, self).validate(clean)

        required_fields = ['title', 'submission_id']
        for field in required_fields:
            value = getattr(self, field, None)
            if not value:
                raise ValidationError(f"The {field.replace('_', ' ')} field is mandatory.")
            
        
        length_validations = {'title': 255, 'submission_id': 10}

        for field, max_length in length_validations.items():
            value = getattr(self, field, None)
            if max_length is not None and value and len(value) > max_length:
                raise ValidationError(f"The {field.replace('_', ' ')} field must not exceed {max_length} characters.")
            
            min_length = getattr(self, f"min_{field}", None)
            if min_length is not None and value and len(value) < min_length:
                raise ValidationError(f"The {field.replace('_', ' ')} field must be at least {min_length} characters.")


class UserRole(Enum):
    ADMIN = 'admin'
    READER = 'reader'
    JM = 'jm'
    AUTHOR = 'author'


class User(Document):
    name = StringField(required=True, max_length=90)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=8)
    user_role = EnumField(UserRole, default=UserRole.READER)
    profile = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def validate(self, clean=True):
        from app.repository.user import UserRepository
        user_repo = UserRepository(current_app.database)
        self.data = user_repo
        super(User, self).validate(clean)

        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            value = getattr(self, field, None)
            if not value:
                raise ValidationError(f"The {field.replace('_', ' ')} field is mandatory.")
            
        try:
            user_email = self.data.find_by_email(self.email)
            if(user_email):
                raise ValidationError("The EMAIL must be unique.")
        except DoesNotExist:
            pass
        
        length_validations = {'name': 90}

        for field, max_length in length_validations.items():
            value = getattr(self, field, None)
            if max_length is not None and value and len(value) > max_length:
                raise ValidationError(f"The {field.replace('_', ' ')} field must not exceed {max_length} characters.")
            
            min_length = getattr(self, f"min_{field}", None)
            if min_length is not None and value and len(value) < min_length:
                raise ValidationError(f"The {field.replace('_', ' ')} field must be at least {min_length} characters.")
            
        if not self.user_role:
            self.user_role = UserRole.READER.value
