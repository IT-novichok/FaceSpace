from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from ..database import db


class Action(db.Model):
    __tablename__ = 'actions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    subject_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("users.id"))
    object_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("advertisements.id"))
    type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    params = sqlalchemy.Column(sqlalchemy.JSON)
    subject = orm.relationship('User', back_populates='advertisements')
    object = orm.relationship('Advertisement', back_populates='advertisements')
