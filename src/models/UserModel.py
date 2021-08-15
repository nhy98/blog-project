import flask_login

from src.app import db
import datetime
import uuid

from src.config.Constants import UserRole


class UserModel(db.Model, flask_login.UserMixin):
    """
    User Model
    Created by: NHYEN
    Created at: 11/08/2021
    """

    __tablename__ = 'User'

    id = db.Column('UserId', db.String(36), primary_key=True)
    email = db.Column('Email', db.String(50))
    name = db.Column('Name', db.String(100))
    mobile = db.Column('Mobile', db.String(20))
    role = db.Column('Role', db.Integer)
    occupation = db.Column('Occupation', db.String(50))
    account_type = db.Column('AccountType', db.Integer)
    created_at = db.Column('CreatedDate', db.DateTime)
    modified_at = db.Column('ModifiedDate', db.DateTime)
    fb_user_id = db.Column('FbUserId', db.String(20))
    posts = db.relationship('PostModel', backref='User', lazy=True)
    interactions = db.relationship('InteractionModel', backref='User', lazy=True)

    def __init__(self, data):
        self.id = str(uuid.uuid4()) if 'id' not in data else data.get('id')
        self.email = data.get('email')
        self.account_type = data.get('account_type')
        self.name = data.get('name')
        self.mobile = data.get('mobile')
        self.occupation = data.get('occupation')
        self.fb_user_id = data.get('fb_user_id')
        self.role = UserRole.Member
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'mobile': self.mobile,
            'role': self.role,
            'fb_user_id': self.fb_user_id,
            'occupation': self.occupation,
            'account_type': self.account_type,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get(user_id):
        return UserModel.query.get(user_id)

    @staticmethod
    def get_all_user():
        return UserModel.query.all()

    @staticmethod
    def get_by_email(email):
        return UserModel.query.filter(UserModel.email == email).first()

    @staticmethod
    def get_by_fb_user(fb_user_id):
        return UserModel.query.filter(UserModel.fb_user_id == fb_user_id).first()
