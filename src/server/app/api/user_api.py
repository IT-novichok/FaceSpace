from flask import Blueprint, make_response, jsonify, request

from ..errors import DataFormatError, NotFoundError
from ..services import user_service

blueprint = Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    user = user_service.get_user(user_id)
    if user is None:
        return make_response(jsonify({'message': 'User not found!'}), 404)
    else:
        return make_response(jsonify(user.get_profile()), 200)


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    try:
        user_service.create_user(request.get_json())
        return make_response(jsonify({'message': 'success'}), 200)
    except DataFormatError as e:
        return make_response(jsonify({'message': str(e)}), 400)


@blueprint.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    try:
        user_service.update_user(user_id, request.get_json())
        return make_response(jsonify({'message': 'success'}), 200)
    except NotFoundError as e:
        return make_response(jsonify({'message': str(e)}), 404)
    except DataFormatError as e:
        return make_response(jsonify({'message': str(e)}), 400)


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    try:
        user_service.delete_user(user_id)
        return make_response(jsonify({'message': 'success'}), 200)
    except NotFoundError as e:
        return make_response(jsonify({'message': str(e)}), 404)