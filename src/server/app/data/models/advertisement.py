from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from ..database import db

DEFAULT_COVER = """data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4NCjwhLS0gR2VuZXJhdG9yOiBBZG9iZSBJbGx1c3RyYXRvciAyNy4yLjAsIFNWRyBFeHBvcnQgUGx1Zy1JbiAuIFNWRyBWZXJzaW9uOiA2LjAwIEJ1aWxkIDApICAtLT4NCjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0ibGF5ZXIxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCINCgkgdmlld0JveD0iMCAwIDEyOCAxMjgiIHN0eWxlPSJlbmFibGUtYmFja2dyb3VuZDpuZXcgMCAwIDEyOCAxMjg7IiB4bWw6c3BhY2U9InByZXNlcnZlIj4NCjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+DQoJLnN0MHtmaWxsOiMzNkE5RTE7c3Ryb2tlOiMzNkE5RTE7c3Ryb2tlLXdpZHRoOjQ7c3Ryb2tlLW1pdGVybGltaXQ6MTA7fQ0KCS5zdDF7ZmlsbDpub25lO3N0cm9rZTojMzZBOUUxO3N0cm9rZS13aWR0aDo0O3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1taXRlcmxpbWl0OjEwO30NCgkuc3Qye2ZpbGw6bm9uZTtzdHJva2U6IzAwMDAwMDtzdHJva2Utd2lkdGg6NDtzdHJva2UtbWl0ZXJsaW1pdDoxMDt9DQoJLnN0M3tmaWxsOiMzNkE5RTE7c3Ryb2tlOiMzNkE5RTE7c3Ryb2tlLXdpZHRoOjM7c3Ryb2tlLW1pdGVybGltaXQ6MTA7fQ0KCS5zdDR7ZmlsbDpub25lO3N0cm9rZTojMzZBOUUxO3N0cm9rZS13aWR0aDozO3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1taXRlcmxpbWl0OjEwO30NCjwvc3R5bGU+DQo8cGF0aCBjbGFzcz0ic3QwIiBkPSJNNzMsNjUuOGMwLjEsNS42LTQuNCwxMi40LTkuNCwxMi4yYy01LTAuMi04LjctNi45LTguNi0xMi4yYzAtMS4zLDAuMi02LjIsNC41LTguNWMyLjgtMS41LDYuNC0xLjQsOS4xLDAuMQ0KCUM3Mi45LDU5LjcsNzMsNjQuNyw3Myw2NS44eiIvPg0KPHBhdGggY2xhc3M9InN0MSIgZD0iTTQzLjcsOTQuOWMwLjMtMC42LDYuNC0xMi4zLDE5LjYtMTIuNGM4LjQsMCwxNi44LDIuOCwyMSwxMi40Ii8+DQo8cGF0aCBjbGFzcz0ic3QyIiBkPSJNNTYuNiw2Mi44Ii8+DQo8Y2lyY2xlIGNsYXNzPSJzdDEiIGN4PSI2NCIgY3k9IjgwIiByPSIzMCIvPg0KPHBhdGggY2xhc3M9InN0MCIgZD0iTTM5LjIsNDIuNmMwLjEsNC41LTMuNSw5LjktNy42LDkuOGMtNC0wLjEtNy01LjUtNi45LTkuOGMwLTEsMC4xLTUsMy42LTYuOGMyLjItMS4yLDUuMS0xLjIsNy4zLDAuMQ0KCUMzOS4xLDM3LjgsMzkuMiw0MS43LDM5LjIsNDIuNnoiLz4NCjxwYXRoIGNsYXNzPSJzdDEiIGQ9Ik0xNS44LDY1LjljMC4yLTAuNSw1LjEtOS44LDE1LjctOS45YzIsMCwzLjksMC4yLDUuOCwwLjYiLz4NCjxwYXRoIGNsYXNzPSJzdDEiIGQ9Ik0yOCw3Ny43QzE2LjcsNzUuOCw4LDY1LjksOCw1NGMwLTEzLjMsMTAuNy0yNCwyNC0yNGM5LjYsMCwxNy44LDUuNiwyMS43LDEzLjciLz4NCjxwYXRoIGNsYXNzPSJzdDMiIGQ9Ik04OS4xLDI3LjRjMCwzLTIuMyw2LjYtNSw2LjVjLTIuNi0wLjEtNC43LTMuNy00LjYtNi41YzAtMC43LDAuMS0zLjMsMi40LTQuNmMxLjUtMC44LDMuNC0wLjgsNC45LDANCglDODksMjQuMSw4OS4xLDI2LjgsODkuMSwyNy40eiIvPg0KPHBhdGggY2xhc3M9InN0NCIgZD0iTTczLjUsNDIuOWMwLjItMC4zLDMuNC02LjYsMTAuNC02LjZjNC41LDAsOSwxLjUsMTEuMiw2LjYiLz4NCjxjaXJjbGUgY2xhc3M9InN0NCIgY3g9Ijg0LjMiIGN5PSIzNC45IiByPSIxNiIvPg0KPC9zdmc+DQo="""
class Advertisement(db.Model, SerializerMixin):
    __tablename__ = 'advertisements'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    publisher_id = sqlalchemy.Column(sqlalchemy.Integer,
                                     sqlalchemy.ForeignKey("users.id"))
    cover = sqlalchemy.Column(sqlalchemy.String, default=DEFAULT_COVER)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))
    popularity = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    publication_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=datetime.now())
    banned = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    publisher = orm.relationship('User', back_populates='advertisements')
    category = orm.relationship('Category', back_populates='advertisements')
    actions = orm.relationship('Action', back_populates='object')
    likes = orm.relationship('Action', primaryjoin='and_(Advertisement.id == Action.object_id, Action.type=="like")',
                             back_populates='object')
    views = orm.relationship('Action', primaryjoin='and_(Advertisement.id == Action.object_id, Action.type=="view")',
                             back_populates='object')
    responses = orm.relationship('Action',
                                 primaryjoin='and_(Advertisement.id == Action.object_id, Action.type=="respond")',
                                 back_populates='object')

    @property
    def likes_count(self):
        return len(self.likes)

    @property
    def views_count(self):
        return len(self.views)

    @property
    def responses_count(self):
        return len(self.responses)
