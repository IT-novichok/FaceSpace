from flask import Blueprint, make_response, jsonify, request
from src.server.app.data import db_session, User

blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).one_or_none()
    if user:
        return make_response(jsonify(), 200)
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)