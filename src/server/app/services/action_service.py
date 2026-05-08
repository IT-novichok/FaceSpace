from ..data import db, User, Action
from ..errors import DataFormatError, NotFoundError
from . import user_service, advertisement_service
from typing import Any


def get_action(subject_id: int, object_id: int, type: str):
    return db.session.query(Action).filter(Action.subject_id == subject_id, Action.object_id == object_id).first()


def act(subject_id: int, object_id: int, type: str):
    subject = user_service.get_user(subject_id)
    if not subject:
        raise NotFoundError('Subject not found!')
    object = advertisement_service.get_advertisement(object_id)
    if not object:
        raise NotFoundError('Object not found!')
    action = Action(
        subject=subject,
        object=object,
        type=type
    )
    db.session.add(action)
    db.commit()


def view_advertisement(subject_id: int, object_id: int):
    view = get_action(subject_id, object_id, 'view')
    if not view:
        act(subject_id, object_id, 'view')


def like_advertisement(subject_id: int, object_id: int):
    like = get_action(subject_id, object_id, 'like')
    if not like:
        act(subject_id, object_id, 'like')


def delete_action(subject_id: int, object_id: int, type: str):
    action = get_action(subject_id, object_id, type)
    if not action:
        raise NotFoundError('Action not found!')
    else:
        db.session.delete(action)
        db.commit()


def delete_like(subject_id: int, object_id: int):
    action = get_action(subject_id, object_id, 'like')
    if not action:
        raise NotFoundError('Action not found!')
    else:
        db.session.delete(action)
        db.commit()
