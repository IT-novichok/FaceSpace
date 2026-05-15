from flask import Blueprint, make_response, jsonify, request
from flask_login import current_user

from ..errors import DataFormatError, NotFoundError
from ..services import advertisement_service, action_service

blueprint = Blueprint(
    'advertisement_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/advertisement/<int:id>', methods=['GET'])
def get_advertisement(id: int):
    advertisement = advertisement_service.get_advertisement(id)
    if advertisement is None:
        return make_response(jsonify({'message': 'Advertisement not found!'}), 404)
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


@blueprint.route('/api/advertisement/<int:id>/like', methods=['POST'])
def like(id: int):
    try:
        action_service.like(id, request.get_json()['user_id'])
        return make_response(jsonify({'message': 'success'}), 200)
    except NotFoundError as e:
        return make_response(jsonify({'message': str(e)}), 404)


@blueprint.route('/api/advertisement/<int:id>/like', methods=['DELETE'])
def unlike(id: int):
    try:
        action_service.unlike(request.get_json()['user_id'], id)
        return make_response(jsonify({'message': 'success'}), 200)
    except NotFoundError as e:
        return make_response(jsonify({'message': str(e)}), 404)


@blueprint.route('/api/advertisement/<int:id>/respond', methods=['POST'])
def respond(id: int):
    try:
        action_service.respond(request.get_json()['user_id'], id)
        return make_response(jsonify({'message': 'success'}), 200)
    except NotFoundError as e:
        return make_response(jsonify({'message': str(e)}), 404)


@blueprint.route('/api/advertisement/<int:id>/respond', methods=['DELETE'])
def unrespond(id: int):
    try:
        action_service.unrespond(request.get_json()['user_id'], id)
        return make_response(jsonify({'message': 'success'}), 200)
    except NotFoundError as e:
        return make_response(jsonify({'message': str(e)}), 404)


@blueprint.route('/api/advertisement/<int:id>/view', methods=['POST'])
def view(id: int):
    try:
        action_service.view(request.get_json()['user_id'], id)
        return make_response(jsonify({'message': 'success'}), 200)
    except NotFoundError as e:
        return make_response(jsonify({'message': str(e)}), 404)
