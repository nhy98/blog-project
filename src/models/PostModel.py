import uuid
from src.app import db
import datetime


class PostModel(db.Model):
    """
    Post Model
    Created by: NHYEN
    Created at: 11/08/2021
    """

    __tablename__ = 'Post'

    id = db.Column('PostId', db.String(36), primary_key=True)
    user_id = db.Column('UserId', db.String(36), db.ForeignKey('User.UserId'))
    title = db.Column('Title', db.String(50))
    content = db.Column('Content', db.Text)
    created_at = db.Column('CreatedDate', db.DateTime)
    modified_at = db.Column('ModifiedDate', db.DateTime)
    interactions = db.relationship('InteractionModel', backref='Post', lazy=True)

    def __init__(self, data):
        self.id = str(uuid.uuid4()) if 'id' not in data else data.get('id')
        self.user_id = data.get('user_id')
        self.title = data.get('title')
        self.content = data.get('content')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
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
    def get_all_blogposts():
        return PostModel.query.all()

    @staticmethod
    def get_one_blogpost(post_id):
        return PostModel.query.get(post_id)

    @staticmethod
    def get_blogpost_by_user(user_id):
        return PostModel.query.filter(PostModel.user_id == user_id).all()
