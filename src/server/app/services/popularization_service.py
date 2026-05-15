from ..data import db, Advertisement
from . import advertisement_service
from ..errors import NotFoundError


def popularize(id: int, rate:int):
    advertisement = advertisement_service.get_advertisement(id)
    if not advertisement:
        return NotFoundError('Advertisement not found')
    else:
        advertisement.popularity += rate
        db.session.commit()
def dispopularize(id: int, rate:int):
    advertisement = advertisement_service.get_advertisement(id)
    if not advertisement:
        return NotFoundError('Advertisement not found')
    else:
        advertisement.popularity -= rate
        db.session.commit()
