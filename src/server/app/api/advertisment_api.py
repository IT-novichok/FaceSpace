from flask import Blueprint, make_response, jsonify, request

from ..errors import DataFormatError, NotFoundError
from ..services import advertisement_service

blueprint = Blueprint(
    'advertisement_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/advertisement/<int:id>', methods=['GET'])
def get_user(id: int):
    advertisement = advertisement_service.get_advertisement(id)
    if advertisement is None:
        return make_response(jsonify({'message': 'User not found!'}), 404)
    else:
        return make_response(jsonify(advertisement.to_dict()), 200)


@blueprint.route('/api/advertisement', methods=['POST'])
def create_advertisement():
    try:
        advertisement_service.create_advertisement(request.get_json())
        return make_response(jsonify({'message': 'success'}), 200)
    except DataFormatError as e:
        return make_response(jsonify({'message': str(e)}), 400)


@blueprint.route('/api/advertisement/<int:id>', methods=['PUT'])
def update_advertisement(id: int):
    try:
        advertisement_service.update_advertisement(id, request.get_json())
        return make_response(jsonify({'message': 'success'}), 200)
    except NotFoundError as e:
        return make_response(jsonify({'message': str(e)}), 404)
    except DataFormatError as e:
        return make_response(jsonify({'message': str(e)}), 400)


@blueprint.route('/api/advertisement/<int:id>', methods=['DELETE'])
def delete_advertisement(id: int):
    try:
        advertisement_service.delete_advertisement(id)
        return make_response(jsonify({'message': 'success'}), 200)
    except NotFoundError as e:
        return make_response(jsonify({'message': str(e)}), 404)
