from marshmallow import Schema, fields, validate


class GroupSchema(Schema):
    group_name = fields.String(required=True, validate=validate.Length(min=3, max=255))
    group_link = fields.String(required=True, validate=validate.URL)


class GroupLinkSchema(Schema):
    group_link = fields.String(required=True, validate=validate.URL)


class UpdateGroupSchema(Schema):
    group_name = fields.String(validate=validate.Length(min=3, max=255))
    group_link = fields.String(validate=validate.URL)
