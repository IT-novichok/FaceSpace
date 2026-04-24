from flask import Blueprint, make_response, jsonify, request
from src.server.app.data import db, User

blueprint = Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    user = db.session.query(User).filter(User.id == user_id).one_or_none()
    if user:
        return make_response(jsonify(user.get_profile()), 200)
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(
            key in request.json for key in ['name', 'nickname', 'email', 'birth_date', 'gender', 'about', 'password']):
        return make_response(jsonify({'error': 'Empty request'}), 400)
    else:
        user = User(
            name=request.json['name'],
            nickname=request.json['nickname'],
            email=request.json['email'],
            birth_date=request.json['birth_date'],
            gender=request.json['gender'],
            about=request.json['about'],
        )
        user.set_password(request.json['data'])
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'message': 'success'}), 200)


@blueprint.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({'message': 'success'}), 200)
    elif not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    else:
        return make_response(jsonify({'message': 'success'}), 200)


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).one_or_none()
    if user:
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({'message': 'success'}), 200)
    else:
        return make_response(jsonify({'error': 'Not found'}), 200)
