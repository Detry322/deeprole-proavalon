import os
from flask import Blueprint, request

from util import require_auth_decorator, CAPABILITIES, get_missing_fields, matches_capabilities, quickhash
from keyvalue import STORE
from lookup_tables import get_deeprole_perspective
from game import replay_game_and_run_deeprole, get_move

import requests
import json

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

    num_players = request.data['numPlayers']
    players = request.data['players']
    name = request.data['name']
    player = players.index(name)
    role = request.data['role']
    spies = request.data.get('see', {}).get('spies', [])
    spies = [ players.index(spy) for spy in spies ]
    team_leader = request.data['teamLeader']
    perspective = get_deeprole_perspective(player, role, spies)

    session_id = "session:" + os.urandom(10).hex()
    session_info = {
        'session_id': session_id,
        'num_players': num_players,
        'name': name,
        'player': player,
        'players': players,
        'starting_proposer': team_leader,
        'perspective': perspective,
        'nodes_in_use': [],
    }

    STORE.set(session_id, session_info)
    return {
        'sessionID': session_id
    }


@deeprole_app.route('/v0/session/act', methods=['POST'])
@require_auth_decorator
def get_action():
    if not isinstance(request.data, dict):
        raise exceptions.ParseError('Data is not a json dict')
    missing_fields = get_missing_fields(request.data, ['sessionID', 'gameInfo'])
    if len(missing_fields) != 0:
        raise exceptions.ParseError('Data is missing fields: {}'.format(missing_fields))
    game_info = request.data['gameInfo']
    missing_fields = get_missing_fields(game_info, ['voteHistory', 'phase', 'teamLeader', 'pickNum'])
    if len(missing_fields) != 0:
        raise exceptions.ParseError('gameInfo is missing fields: {}'.format(missing_fields))
    session_id = request.data['sessionID']
    try:
        session_info = STORE.get(session_id)
    except ValueError:
        raise exceptions.NotFound('Could not find session ID: {}'.format(session_id))

    current_node = replay_game_and_run_deeprole(session_info, game_info)

    return get_move(game_info['phase'], session_info, current_node)


@deeprole_app.route('/v0/session/gameover', methods=['POST'])
@require_auth_decorator
def gameover():
    if not isinstance(request.data, dict):
        raise exceptions.ParseError('Data is not a json dict')
    missing_fields = get_missing_fields(request.data, ['sessionID', 'gameInfo'])
    if len(missing_fields) != 0:
        raise exceptions.ParseError('Data is missing fields: {}'.format(missing_fields))
    session_id = request.data['sessionID']
    try:
        session_info = STORE.get(session_id)
    except ValueError:
        raise exceptions.NotFound('Could not find session ID: {}'.format(session_id))

    for node_id in session_info['nodes_in_use']:
        new_count = STORE.refcount_decr(node_id)
        if new_count == 0:
            STORE.delete(node_id)

    STORE.delete(session_id)

    url = 'https://jserrino.scripts.mit.edu/datasink/index.py?auth_key={}'.format(os.environ.get('SECRET_AUTH_KEY'))
    r = requests.post(url, headers={ 'Content-Type': 'application/json' }, data=json.dumps({
        'session_info': session_info,
        'game_info': request.data['gameInfo']
    }))

    return r.json()
