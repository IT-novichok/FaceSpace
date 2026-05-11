from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from ..database import db


class Advertisement(db.Model, SerializerMixin):
    __tablename__ = 'advertisements'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    publisher_id = sqlalchemy.Column(sqlalchemy.Integer,
                                     sqlalchemy.ForeignKey("users.id"))
    cover = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))
    popularity = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    publication_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=datetime.now())
    banned = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    publisher = orm.relationship('User', back_populates='advertisements')
    category = orm.relationship('Category', back_populates='advertisements')
    actions = orm.relationship('Action', back_populates='object')
    likes = orm.relationship('Action', primaryjoin='and_(Advertisement.id == Action.object_id, Action.type=="like")',
                             back_populates='object')
    views = orm.relationship('Action', primaryjoin='and_(Advertisement.id == Action.object_id, Action.type=="view")',
                             back_populates='object')
    responses = orm.relationship('Action',
                                 primaryjoin='and_(Advertisement.id == Action.object_id, Action.type=="respond")',
                                 back_populates='object')

    @property
    def likes_count(self):
        return len(self.likes)

    @property
    def views_count(self):
        return len(self.views)

    @property
    def responses_count(self):
        return len(self.responses)