from ..data import db, Advertisement, Category
from ..errors import DataFormatError, NotFoundError
from typing import Any


def check_data(data: dict):
    if data.get('title'):
        if len(data['title']) > 50:
            raise DataFormatError("Title must be less than 50 characters")


def get_advertisement(id: int) -> Advertisement:
    return db.session.get(Advertisement, id)


def get_all_advertisements() -> list[Advertisement]:
    return db.session.query(Advertisement).order_by(Advertisement.popularity.desc()).all()


def create_advertisement(data: dict[str, Any]):
    check_data(data)
    advertisement = Advertisement()
    try:
        advertisement.cover = data['cover'] or advertisement.cover
        advertisement.title = data['title']
        advertisement.publisher_id = data['publisher_id']
        advertisement.content = data['content']
        advertisement.category_id = data['category_id']
    except KeyError as e:
        raise DataFormatError(f"Missing required data: {e}")
    db.session.add(advertisement)
    db.session.commit()


def update_advertisement(id: int, data: dict[str, Any]):
    advertisement = get_advertisement(id)
    if not advertisement:
        raise NotFoundError('Advertisement not found!')
    else:
        check_data(data)
        advertisement.cover = data.get('cover') or advertisement.cover
        advertisement.title = data.get('title') or advertisement.title
        advertisement.publisher_id = data.get('publisher_id') or advertisement.publisher_id
        advertisement.content = data.get('content') or advertisement.content
        advertisement.category_id = data.get('category_id') or advertisement.category_id
        db.session.commit()


def delete_advertisement(id: int):
    advertisement = get_advertisement(id)
    if not advertisement:
        raise NotFoundError('Advertisement not found!')
    else:
        db.session.delete(advertisement)
        db.session.commit()
