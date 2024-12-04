from flask import Blueprint

backend_blueprint = Blueprint("backend_blueprint", __name__)

@backend_blueprint.route('/test', methods=['GET'])
def test():
    bruh = "hi"
    return bruh

