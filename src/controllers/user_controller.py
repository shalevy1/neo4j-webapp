from flask import jsonify, Blueprint
from src.models.user import User
from src.errors import Error, StatusCode
from src.schemas.user_schema import UserSchema, UpdateUserSchema
from src.schemas.work_schema import WorkSchema, WorkLinkSchema
from src.schemas.group_schema import GroupLinkSchema
from src.utils.helpers import parse_request_args

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
@parse_request_args(UserSchema())
def add_user(args):
    user = User.get_user(args['user_id'])
    if user is not None:
        raise Error(StatusCode.BAD_REQUEST, 'User is already existed')
    if 'user_basic_info' not in args:
        args['user_basic_info'] = None
    if 'user_contact_info' not in args:
        args['user_contact_info'] = None
    if 'user_relationship_info' not in args:
        args['user_relationship_info'] = None
    user = User.add_user(args['user_id'], args['username'], args['user_basic_info'], args['user_contact_info'], args['user_relationship_info'])
    return jsonify({
        'status': True,
        'user': user
    }), StatusCode.OK


@user_blueprint.route('/users/<user_id>', methods=['PUT'])
@parse_request_args(UpdateUserSchema())
def update_user(user_id, args):
    user = User.get_user(user_id)
    if user is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot find user')
    if 'user_id' not in args:
        args['user_id'] = user['user_id']
    if 'username' not in args:
        args['username'] = user['username']
    if 'user_basic_info' not in args:
        args['user_basic_info'] = user['user_basic_info']
    if 'user_contact_info' not in args:
        args['user_contact_info'] = user['user_contact_info']
    if 'user_relationship_info' not in args:
        args['user_relationship_info'] = user['user_relationship_info']
    new_user_id = args['user_id']
    user = User.get_user(new_user_id)
    if user_id != new_user_id and user is not None:
        raise Error(StatusCode.BAD_REQUEST, 'User ID is already existed')
    user = User.update_user(user_id, new_user_id, args['username'], args['user_basic_info'], args['user_contact_info'], args['user_relationship_info'])
    return jsonify({
        'status': True,
        'user': user
    }), StatusCode.OK


@user_blueprint.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.get_user(user_id)
    if user is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot find user')
    User.delete_user(user_id)
    return jsonify({
        'status': True,
        'message': 'Delete user successfully'
    })


@user_blueprint.route('/users/<user_id>/works', methods=['GET'])
def get_user_works(user_id):
    user = User.get_user(user_id)
    if user is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot find user')
    works = User.get_user_works(user_id)
    return jsonify({
        'status': True,
        'works': works
    }), StatusCode.OK


@user_blueprint.route('/users/<user_id>/works', methods=['POST'])
@parse_request_args(WorkSchema())
def add_user_work(user_id, args):
    user = User.get_user(user_id)
    if user is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot found user')
    if 'work_place_link' not in args:
        args['work_place_link'] = None
    work = User.add_user_work(user_id, args['work_place_name'], args['work_place_link'])
    return jsonify({
        'status': True,
        'work': work
    }), StatusCode.OK


@user_blueprint.route('/users/<user_id>/works', methods=['DELETE'])
@parse_request_args(WorkLinkSchema())
def delete_user_work(user_id, args):
    user = User.get_user(user_id)
    if user is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot found user')
    User.delete_user_work(user_id, args['work_place_link'])
    return jsonify({
        'status': True,
        'message': 'Delete work successfully'
    }), StatusCode.OK


@user_blueprint.route('/users/<user_id>/groups', methods=['GET'])
def get_user_groups(user_id):
    user = User.get_user(user_id)
    if user is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot found user')
    groups = User.get_user_groups(user_id)
    return jsonify({
        'status': True,
        'groups': groups
    }), StatusCode.OK


@user_blueprint.route('/users/<user_id>/groups/', methods=['POST'])
@parse_request_args(GroupLinkSchema())
def join_group(user_id, args):
    user = User.get_user(user_id)
    if user is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot found user')
    User.join_group(user_id, args['group_link'])
    return jsonify({
        'status': True,
        'message': 'Join group successfully'
    }), StatusCode.OK


@user_blueprint.route('/users/<user_id>/groups/', methods=['DELETE'])
@parse_request_args(GroupLinkSchema())
def leave_group(user_id, args):
    user = User.get_user(user_id)
    if user is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot found user')
    User.leave_group(user_id, args['group_link'])
    return jsonify({
        'status': True,
        'message': 'Leave group successfully'
    }), StatusCode.OK
