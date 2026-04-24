import sqlalchemy
from ..database import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    popularity = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
