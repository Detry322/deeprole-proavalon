from flask import Blueprint

from util import require_auth_decorator, CAPABILITIES, get_missing_fields, matches_capabilities

deeprole_app = Blueprint('deeprole', __name__)

@deeprole_app.route('/v0/info', methods=['GET'])
def get_info():
    return {
        "name": "DeepRole",
        "chat": False,
        "capabilities": CAPABILITIES
    }


@deeprole_app.route('/v0/session', methods=['POST'])
@require_auth_decorator
def create_session():
    if not isinstance(request.data, dict):
        raise exceptions.ParseError('Data is not a json dict')
    missing_fields = get_missing_fields(
        request.data, ['numPlayers', 'roles', 'cards', 'teamLeader',
                       'players', 'name', 'role']
    )
    if len(missing_fields) != 0:
        raise exceptions.ParseError('Data is missing fields: {}'.format(missing_fields))
    if not matches_capabilities(request.data):
        raise exceptions.ParseError("Bot can't handle these capabilities")

    sessionID = os.urandom(10).hex()
    SESSION_DATA[sessionID] = {
        'sessionID': sessionID,
        'creation_data': request.data,
    }
    return {
        'sessionID': sessionID
    }
