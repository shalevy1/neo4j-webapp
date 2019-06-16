from flask import render_template, Blueprint, request, jsonify

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route('/')
def index():
    return render_template('index.html')
