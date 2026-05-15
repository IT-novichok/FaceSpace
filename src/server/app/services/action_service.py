from ..data import db, User, Action
from ..errors import DataFormatError, NotFoundError
from . import user_service, advertisement_service, popularization_service
action_ratings  = {
    'view':1,
    'like': 3,
    'respond':5,
}
def get_action(subject_id: int, object_id: int, type: str):
    return db.session.query(Action).filter(Action.subject_id == subject_id, Action.object_id == object_id,
                                           Action.type == type).first()


def add_action(subject_id: int, object_id: int, type: str):
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
    db.session.commit()


def delete_action(subject_id: int, object_id: int, type: str):
    action = get_action(subject_id, object_id, type)
    if not action:
        raise NotFoundError('Action not found!')
    else:
        db.session.delete(action)
        db.session.commit()


def view(subject_id: int, object_id: int):
    view = get_action(subject_id, object_id, 'view')
    if not view:
        popularization_service.popularize(object_id, action_ratings['view'])
        add_action(subject_id, object_id, 'view')


def like(subject_id: int, object_id: int):
    like = get_action(subject_id, object_id, 'like')
    if not like:
        popularization_service.popularize(object_id, action_ratings['like'])
        add_action(subject_id, object_id, 'like')


def respond(subject_id: int, object_id: int):
    response = get_action(subject_id, object_id, 'respond')
    if not response:
        popularization_service.popularize(object_id, action_ratings['respond'])
        add_action(subject_id, object_id, 'respond')


def unlike(subject_id: int, object_id: int):
    like = get_action(subject_id, object_id, 'like')
    if like:
        popularization_service.dispopularize(object_id, action_ratings['like'])
        delete_action(subject_id, object_id, 'like')


def unrespond(subject_id: int, object_id: int):
    response = get_action(subject_id, object_id, 'respond')
    if response:
        popularization_service.dispopularize(object_id, action_ratings['respond'])
        delete_action(subject_id, object_id, 'respond')
