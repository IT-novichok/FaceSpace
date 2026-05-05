from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from ..database import db


class Advertisement(db.Model):
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
