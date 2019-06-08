from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    user_id = fields.String(required=True, validate=validate.Length(min=3, max=50))
    username = fields.String(required=True, validate=validate.Length(min=3, max=255))
    user_basic_info = fields.String()
    user_contact_info = fields.String()
    user_relationship_info = fields.String()


class UpdateUserSchema(Schema):
    user_id = fields.String(validate=validate.Length(min=3, max=50))
    username = fields.String(validate=validate.Length(min=3, max=255))
    user_basic_info = fields.String()
    user_contact_info = fields.String()
    user_relationship_info = fields.String()
