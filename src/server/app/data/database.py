from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Database(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Database)
