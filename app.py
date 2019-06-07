from flask import Flask, g, jsonify
import logging
from src.errors import Error
from src.controllers.user_controller import user_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint)


@app.teardown_appcontext
def close_db(exception):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()


@app.errorhandler(404)
def handle_not_found(exception):
    """Handle an invalid endpoint"""
    return jsonify({
        'message': 'Resource not found'
    }), 404


@app.errorhandler(Error)
def handle_exception(error):
    return error.to_response()


@app.errorhandler(500)
def handle_internal_error(exception):
    """Rollback database transaction if any error occurs"""
    logging.error(exception)
    #db.session.rollback()
    return jsonify({
        'message': 'An unexpected internal error has occurred'
    }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
