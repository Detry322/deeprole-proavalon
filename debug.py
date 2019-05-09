from flask import Blueprint, request
from flask import current_app as app
from flask_api import exceptions
import os
import random

from util import require_auth_decorator, CAPABILITIES, get_missing_fields, matches_capabilities

debug_app = Blueprint('debug', __name__)

SESSION_DATA = {}

@debug_app.route('/v0/info', methods=['GET'])
def get_info():
    return {
        "name": "DebugRole",
        "chat": False,
        "capabilities": CAPABILITIES
    }


@debug_app.route('/v0/session', methods=['POST'])
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


@debug_app.route('/v0/session/act', methods=['POST'])
@require_auth_decorator
def bot_action():
    if not isinstance(request.data, dict):
        raise exceptions.ParseError('Data is not a json dict')
    missing_fields = get_missing_fields(request.data, ['sessionID', 'gameInfo'])
    if len(missing_fields) != 0:
        raise exceptions.ParseError('Data is missing fields: {}'.format(missing_fields))
    session_id = request.data['sessionID']
    if session_id not in SESSION_DATA:
        raise exceptions.NotFound('Could not find session ID: {}'.format(session_id))

    creation_data = SESSION_DATA[session_id]['creation_data']
    game_data = request.data['gameInfo']

    if game_data['phase'] == 'pickingTeam':
        num_players = int(game_data['numPlayersOnMission'][game_data['missionNum']])
        return {
            'buttonPressed': "yes",
            'selectedPlayers': random.sample(creation_data['players'], num_players)
        }
    elif game_data['phase'] == 'votingTeam':
        return {
            'buttonPressed': "yes" if random.random() < 0.5 else "no"
        }
    elif game_data['phase'] == 'votingMission':
        return {
            'buttonPressed': "yes" if random.random() < 0.5 else "no"
        }
    elif game_data['phase'] == 'assassination':
        return {
            'buttonPressed': "yes",
            'selectedPlayers': [
                random.choice(creation_data['players'])
            ]
        }
    else:
        raise exceptions.ParseError("Invalid phase. Must be one of: pickingTeam, votingTeam, votingMission, assassination")


@debug_app.route('/v0/session/gameover', methods=['POST'])
@require_auth_decorator
def gameover():
    if not isinstance(request.data, dict):
        raise exceptions.ParseError('Data is not a json dict')
    missing_fields = get_missing_fields(request.data, ['sessionID', 'gameInfo'])
    if len(missing_fields) != 0:
        raise exceptions.ParseError('Data is missing fields: {}'.format(missing_fields))
    session_id = request.data['sessionID']
    if session_id not in SESSION_DATA:
        raise exceptions.NotFound('Could not find session ID: {}'.format(session_id))

    del SESSION_DATA[session_id]

    return {}
