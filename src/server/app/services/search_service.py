from ..data import db, Advertisement
from sqlalchemy import and_, or_


def search_advertisement(text: str):
    keywords = text.split()
    title_matches = [Advertisement.title.ilike(f'%{keyword}%') for keyword in keywords]
    content_matches = [Advertisement.content.ilike(f'%{keyword}%') for keyword in keywords]
    results = (db.session.query(Advertisement)
               .where(and_(content_matches))
               .order_by(Advertisement.popularity.desc())
               .all())
    return results
