import uuid

from src.app import db
import datetime


class InteractionModel(db.Model):
    """
    Interaction Model
    Created by: NHYEN
    Created at: 11/08/2021
    """

    __tablename__ = 'Interaction'

    id = db.Column('InterId', db.String(36), primary_key=True)
    user_id = db.Column('UserId', db.String(36), db.ForeignKey('User.UserId'), nullable=False)
    post_id = db.Column('PostId', db.String(50), db.ForeignKey('Post.PostId'), nullable=False)
    created_at = db.Column('CreatedDate', db.DateTime)
    modified_at = db.Column('ModifiedDate', db.DateTime)
    is_deleted = db.Column('IsDeleted', db.Integer)

    def __init__(self, data):
        self.id = str(uuid.uuid4())
        self.user_id = data.get('user_id')
        self.post_id = data.get('post_id')
        self.is_deleted = 0
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
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

    def soft_delete(self):
        self.is_deleted = 1
        db.session.commit()

    @staticmethod
    def get(inter_id):
        return InteractionModel.query.get(inter_id)

    @staticmethod
    def get_interaction_by_user_and_post(post_id, user_id=None):
        if user_id:
            return InteractionModel.query.filter(
                InteractionModel.user_id == user_id and InteractionModel.post_id == post_id).filter(
                InteractionModel.is_deleted == 0).first()

        from src.models.UserModel import UserModel
        return InteractionModel.query.join(UserModel, UserModel.id == InteractionModel.user_id).add_columns(
            UserModel.name, UserModel.email, InteractionModel.id).filter(
            InteractionModel.post_id == post_id).filter(
            InteractionModel.is_deleted == 0).all()
