from flask import jsonify, Blueprint
from src.models.user import User
from src.errors import Error, StatusCode

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.get_users()
    #print(users, file=sys.stderr)
    return jsonify({
        'status': True,
        'users': users
    }), StatusCode.OK


@user_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.get_user(user_id)
    if user is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot find user')
    return jsonify({
        'status': True,
        'user': user
    }), StatusCode.OK


@user_blueprint.route('/users', methods=['POST'])
def add_user():
    pass


@user_blueprint.route('/users/<user_id>', methods=['PUT'])
def update_user():
    pass


@user_blueprint.route('/users/<user_id>', methods=['DELETE'])
def delete_user():
    pass
