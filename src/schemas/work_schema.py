from marshmallow import Schema, fields, validate


class WorkSchema(Schema):
    work_place_name = fields.String(required=True, validate=validate.Length(min=3, max=255))
    work_place_link = fields.String(validate=validate.URL)


class WorkLinkSchema(Schema):
    work_place_link = fields.String(required=True ,validate=validate.URL)
