import sqlalchemy
from sqlalchemy import orm
from ..database import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    popularity = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    advertisements = orm.relationship('Advertisement', back_populates='category')
