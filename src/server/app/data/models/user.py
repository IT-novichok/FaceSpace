from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    nickname = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    avatar = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    gender = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    birth_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    contacts = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    registration_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=datetime.now())
    banned = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    advertisements = orm.relationship('Advertisement', back_populates='publisher')
    #actions = orm.relationship('Action', back_populates='subject')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_profile(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'nickname': self.nickname,
            'about': self.about,
            'contacts': self.contacts,
            'email': self.email,
            'avatar': self.avatar,
            'gender': self.gender,
            'birth_date': self.birth_date,
        }
