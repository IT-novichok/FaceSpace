from ..data import db, Advertisement
from sqlalchemy import or_


def search_advertisement(text: str):
    keywords = text.split()
    title_matches = [Advertisement.title.ilike(f'%{keyword}%') for keyword in keywords]
    content_matches = [Advertisement.content.ilike(f'%{keyword}%') for keyword in keywords]
    results = (db.session.query(Advertisement)
               .where(or_(or_(*content_matches), or_(*title_matches)))
               .order_by(Advertisement.popularity.desc())
               .all())
    return results
