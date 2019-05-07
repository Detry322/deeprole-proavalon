from flask import Blueprint

deeprole_app = Blueprint('deeprole', __name__)

@deeprole_app.route('/v0/info', methods=['GET'])
def get_info():
    return {
        "name": "DeepRole",
        "chat": False,
        "capabilities": []
    }
