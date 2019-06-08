from flask import request
from functools import wraps
from src.errors import Error, StatusCode


def parse_request_args(schema):
    def parse_request_args_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            request_args = request.get_json() or {}
            if request.method == 'GET':
                request_args = request.args.to_dict()
            parsed_args, errors = schema.load(request_args)
            if errors:
                raise Error(StatusCode.BAD_REQUEST, 'Bad request', errors)
            kwargs['args'] = parsed_args
            return f(*args, **kwargs)

        return decorated_function

    return parse_request_args_decorator
