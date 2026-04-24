from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from ..database import db


class Advertisement(db.Model):
    __tablename__ = 'advertisements'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    publisher = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("users.id"))
    content = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))
    views = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    responders = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    popularity = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    publication_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=datetime.now())
    banned = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user = orm.relationship('User')