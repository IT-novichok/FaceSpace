from datetime import datetime
import sqlalchemy
from sqlalchemy import orm, Table, Column, ForeignKey, Integer

from ..database import db

interactions_table = Table(
    "interactons",
    db.metadata,
    Column("subject_id", ForeignKey("users.id"), primary_key=True),
    Column("object_id", ForeignKey("advertisements.id"), primary_key=True),
)


class Action(db.Model):
    __tablename__ = 'actions'

    id = Column(Integer,
                primary_key=True, autoincrement=True)
    type = Column(sqlalchemy.String, nullable=False)
    params = Column(sqlalchemy.JSON)
    subject = orm.relationship('User',secondary=interactions_table, back_populates='advertisements')
    object = orm.relationship('Advertisement',secondary=interactions_table, back_populates='advertisements')
