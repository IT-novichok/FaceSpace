from datetime import datetime
import sqlalchemy
from sqlalchemy import Table, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..database import db


class Action(db.Model):
    __tablename__ = 'actions'

    id = Column(Integer,
                primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey('users.id'))
    object_id = Column(Integer, ForeignKey('advertisements.id'))
    type = Column(sqlalchemy.String, nullable=False)
    params = Column(sqlalchemy.JSON)
    subject = relationship('User', back_populates='actions')
    object = relationship('Advertisement', back_populates='actions')
