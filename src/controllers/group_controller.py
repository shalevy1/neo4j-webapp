from flask import jsonify, Blueprint
from src.models.group import Group
from src.errors import Error, StatusCode
from src.schemas.group_schema import GroupSchema, GroupLinkSchema, UpdateGroupSchema
from src.utils.helpers import parse_request_args

group_blueprint = Blueprint('group_blueprint', __name__)


@group_blueprint.route('/groups', methods=['GET'])
def get_groups():
    groups = Group.get_groups()
    return jsonify({
        'status': True,
        'groups': groups
    }), StatusCode.OK


@group_blueprint.route('/groups/<group_id>', methods=['GET'])
def get_group(group_id):
    group = Group.get_group(group_id)
    if group is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot found group')
    return jsonify({
        'status': True,
        'group': group
    }), StatusCode.OK


@group_blueprint.route('/groups/<group_id>/members', methods=['GET'])
def get_group_members(group_id):
    group = Group.get_group(group_id)
    if group is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot found group')
    members = Group.get_group_members(group_id)
    return jsonify({
        'status': True,
        'members': members
    }), StatusCode.OK


@group_blueprint.route('/groups', methods=['POST'])
@parse_request_args(GroupSchema())
def add_group(args):
    group_id = Group.form_group_id(args['group_link'])
    group = Group.get_group(group_id)
    if group is not None:
        raise Error(StatusCode.BAD_REQUEST, 'Group is already existed')
    group = Group.add_group(group_id, args['group_name'])
    return jsonify({
        'status': True,
        'group': group
    }), StatusCode.OK


@group_blueprint.route('/groups/<group_id>', methods=['PUT'])
@parse_request_args(UpdateGroupSchema())
def update_group(group_id, args):
    group = Group.get_group(group_id)
    if group is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot found group')
    if 'group_id' not in args:
        args['group_id'] = group['group_id']
    if 'group_name' not in args:
        args['group_name'] = group['group_name']
    new_group_id = args['group_id']
    group = Group.get_group(new_group_id)
    if new_group_id != group_id and group is not None:
        raise Error(StatusCode.BAD_REQUEST, 'Group ID is already existed')
    group = Group.update_group(group_id, new_group_id, args['group_name'])
    return jsonify({
        'status': True,
        'group': group
    }), StatusCode.OK


@group_blueprint.route('/groups/<group_id>', methods=['DELETE'])
@parse_request_args(GroupLinkSchema())
def delete_group(group_id):
    group = Group.get_group(group_id)
    if group is None:
        raise Error(StatusCode.NOT_FOUND, 'Cannot found group')
    Group.delete_group(group_id)
    return jsonify({
        'status': True,
        'message': 'Delete group successfully'
    }), StatusCode.OK
