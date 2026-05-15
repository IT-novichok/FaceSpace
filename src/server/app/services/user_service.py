from ..data import User, db
from ..errors import DataFormatError, NotFoundError
from typing import Any


def check_data(data: dict[str, Any]):
    if data.get('name'):
        if not data['name'].replace('_', '').isalnum():
            raise DataFormatError('Name must be alpha-numeric!')
    if data.get('email'):
        if not all([s.replace('.', '').isalpha() and s.islower() for s in data['email'].split('@')]):
            raise DataFormatError('Invalid email format!')
        elif get_user_by_email(data['email']):
            raise DataFormatError('This email already exists!')
    if data.get('gender'):
        if not data['gender'] in ['Male', 'Female', 'Other']:
            raise DataFormatError('Gender must be Male/Female/Other!')
    if data.get('password'):
        if not len(data['password']) >= 8:
            raise DataFormatError('Password must be at least 8 characters!')


def get_user(id: int) -> User:
    user = db.session.get(User, id)
    return user


def get_user_by_name(name: str) -> User:
    return db.session.query(User).filter(User.name == name).first()


def get_user_by_email(email: str) -> User:
    return db.session.query(User).filter(User.email == email).first()


def get_all_users() -> list[User]:
    return db.session.query(User).all()


def create_user(data: dict[str, Any]):
    user = User()
    try:
        check_data(data)
        user.name = data['name']
        user.nickname = data.get('nickname') or data['name']
        user.email = data['email']
        user.gender = data['gender']
        user.set_password(data['password'])
        user.birth_date = data['birth_date']
    except KeyError as e:
        raise DataFormatError(f"Missing required key: {e}")
    db.session.add(user)
    db.session.commit()


def update_user(id, data: dict[str, Any]):
    user = get_user(id)
    if not user:
        raise NotFoundError('User not found!')
    else:
        check_data(data)
        user.name = data.get('name') or user.name
        user.nickname = data.get('nickname') or user.nickname
        user.email = data.get('email') or user.email
        user.about = data.get('about') or user.about
        user.contacts = data.get('contacts') or user.contacts
        user.gender = data.get('gender') or user.gender
        user.birth_date = data.get('birth_date') or user.birth_date
        user.avatar = data.get('avatar') or user.avatar
        db.session.commit()
        return user


def delete_user(id: int):
    user = db.session.get(User, id)
    if not user:
        raise NotFoundError('User not found!')
    else:
        db.session.delete(user)
        db.session.commit()
