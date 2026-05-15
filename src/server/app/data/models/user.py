from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash

DEFAULT_AVATAR = """data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4NCjwhLS0gR2VuZXJhdG9yOiBBZG9iZSBJbGx1c3RyYXRvciAyNy4yLjAsIFNWRyBFeHBvcnQgUGx1Zy1JbiAuIFNWRyBWZXJzaW9uOiA2LjAwIEJ1aWxkIDApICAtLT4NCjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0ibGF5ZXIxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCINCgkgdmlld0JveD0iMCAwIDY0IDY0IiBzdHlsZT0iZW5hYmxlLWJhY2tncm91bmQ6bmV3IDAgMCA2NCA2NDsiIHhtbDpzcGFjZT0icHJlc2VydmUiPg0KPHN0eWxlIHR5cGU9InRleHQvY3NzIj4NCgkuc3Qwe2ZpbGw6bm9uZTtzdHJva2U6IzAwMDAwMDtzdHJva2Utd2lkdGg6NjtzdHJva2UtbWl0ZXJsaW1pdDoxMDt9DQoJLnN0MXtmaWxsOm5vbmU7c3Ryb2tlOiMwMDAwMDA7c3Ryb2tlLXdpZHRoOjY7c3Ryb2tlLWxpbmVjYXA6cm91bmQ7c3Ryb2tlLW1pdGVybGltaXQ6MTA7fQ0KPC9zdHlsZT4NCjxwYXRoIGNsYXNzPSJzdDAiIGQ9Ik00NCwyNC4zYzAuMSw3LjMtNS44LDE2LTEyLjYsMTUuOGMtNi42LTAuMi0xMS42LTguOS0xMS40LTE1LjhjMC0xLjYsMC4yLTgsNi0xMWMzLjctMS45LDguNS0xLjksMTIuMSwwLjENCglDNDMuOSwxNi41LDQ0LDIyLjksNDQsMjQuM3oiLz4NCjxwYXRoIGNsYXNzPSJzdDEiIGQ9Ik01LDYyYzAuNC0wLjgsOC41LTE1LjksMjYuMS0xNmMxMS4yLDAsMjIuNCwzLjcsMjcuOSwxNiIvPg0KPC9zdmc+DQo="""
class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    nickname = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    avatar = sqlalchemy.Column(sqlalchemy.String, default=DEFAULT_AVATAR)
    gender = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    birth_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    contacts = sqlalchemy.Column(sqlalchemy.JSON, default= {})
    registration_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=datetime.now())
    banned = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    advertisements = orm.relationship('Advertisement', back_populates='publisher')
    actions = orm.relationship('Action', back_populates='subject')
    likes = orm.relationship('Action', primaryjoin='and_(User.id == Action.subject_id, Action.type=="like")',
                             back_populates='subject')
    views = orm.relationship('Action', primaryjoin='and_(User.id == Action.subject_id, Action.type=="view")',
                             back_populates='subject')
    responses = orm.relationship('Action', primaryjoin='and_(User.id == Action.subject_id, Action.type=="respond")',
                                 back_populates='subject')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
