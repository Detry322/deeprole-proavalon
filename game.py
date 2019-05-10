import numpy as np
import json
import os

from keyvalue import STORE
from util import quickhash
from run import run_deeprole

def proposal_to_bitstring(proposal):
    result = 0
    for p in proposal:
        result |= (1 << p)
    assert result < 32
    return result


def bitstring_to_proposal(bitstring):
    result = ()
    i = 0
    for i in range(5):
        if ((1 << i) & bitstring) != 0:
            result = result + (i, )
    assert len(result) in [2, 3]
    return result


def get_start_node(session_info):
    return {
        "type": "TERMINAL_PROPOSE_NN",
        "succeeds": 0,
        "fails": 0,
        "propose_count": 0,
        "proposer": session_info['starting_proposer'],
        "new_belief": list(np.ones(60)/60.0)
    }

def terminal_propose_to_node_key(terminal_propose_node):
    assert terminal_propose_node['type'] == 'TERMINAL_PROPOSE_NN'
    return "node:" + quickhash({
        'succeeds': terminal_propose_node['succeeds'],
        'fails': terminal_propose_node['fails'],
        'propose_count': terminal_propose_node['propose_count'],
        'proposer': terminal_propose_node['proposer'],
        'belief': terminal_propose_node['new_belief']
    })


def node_is_caught_up(node, game_info):
    phase = game_info['phase']
    if node['type'] == 'TERMINAL_PROPOSE_NN':
        return False

    if node['type'].startswith('TERMINAL_'):
        return True

    if node['succeeds'] + node['fails'] + 1 < game_info['missionNum']:
        return False

    if node['type'] == 'PROPOSE':
        if phase != 'pickingTeam':
            return False

        return node['proposer'] == game_info['teamLeaderReversed']
    elif node['type'] == 'VOTE':
        if phase != 'votingTeam':
            return False

        return node['proposer'] == game_info['teamLeaderReversed']
    elif node['type'] == 'MISSION':
        return phase == 'votingMission'


def replay_game_and_run_deeprole(session_info, game_info):
    current_node = get_start_node(session_info)

    updated_session = False

    while not node_is_caught_up(current_node, game_info):
        round_ = current_node['succeeds'] + current_node['fails']
        if current_node['type'] == 'TERMINAL_PROPOSE_NN':
            next_node_key = terminal_propose_to_node_key(current_node)
            if not STORE.exists(next_node_key):
                current_node = run_deeprole(current_node)
                STORE.set(next_node_key, current_node)
            else:
                current_node = STORE.get(next_node_key)

            if next_node_key not in session_info['nodes_in_use']:
                session_info['nodes_in_use'].append(next_node_key)
                STORE.refcount_incr(next_node_key)
                updated_session = True

        elif current_node['type'] == 'PROPOSE':
            propose_count = current_node['propose_count']
            leader = None
            proposal = []
            for index, name in enumerate(session_info['players']):
                info = game_info['voteHistory'][name][round_][propose_count]
                if 'VHpicked' in info:
                    proposal.append(index)
                if 'VHleader' in info:
                    assert leader is None
                    leader = index
            assert leader == current_node['proposer']

            child_index = current_node['propose_options'].index(proposal_to_bitstring(proposal))
            current_node = current_node['children'][child_index]
        elif current_node['type'] == 'VOTE':
            propose_count = current_node['propose_count']
            proposal = bitstring_to_proposal(current_node['proposal'])
            for player in proposal:
                name = session_info['players'][player]
                assert 'VHpicked' in game_info['voteHistory'][name][round_][propose_count]
            leader_name = session_info['players'][current_node['proposer']]
            assert 'VHleader' in game_info['voteHistory'][leader_name][round_][propose_count]

            up_voters = []
            for index, name in enumerate(session_info['players']):
                info = game_info['voteHistory'][name][round_][propose_count]
                if 'VHapprove' in info:
                    up_voters.append(index)

            child_index = proposal_to_bitstring(up_voters)
            assert 0 <= child_index < 32
            current_node = current_node['children'][child_index] 
        elif current_node['type'] == 'MISSION':
            fails = game_info['numFailsHistory'][round_]
            current_node = current_node['children'][fails]

    if updated_session:
        STORE.set(session_info['session_id'], session_info)

    return current_node
    print(json.dumps(game_info, indent=2, sort_keys=2))



def get_move(phase, session_info, node):
    player = session_info['player']
    perspective = session_info['perspective']

    if phase == 'pickingTeam':
        assert node['type'] == 'PROPOSE'

        propose_strategy = node['propose_strat'][perspective]
        propose_options = node['propose_options']

        index = np.random.choice(len(propose_strategy), p=propose_strategy)
        players = bitstring_to_proposal(propose_options[index])

        return {
            'buttonPressed': 'yes',
            'selectedPlayers': [session_info['players'][p] for p in players]
        }
    elif phase == 'votingTeam':
        assert node['type'] == 'VOTE'

        vote_strategy = node['vote_strat'][player][perspective]
        vote_up = bool(np.random.choice(len(vote_strategy), p=vote_strategy))
        return {
            'buttonPressed': 'yes' if vote_up else 'no'
        }
    elif phase == 'votingMission':
        assert node['type'] == 'MISSION'

        if perspective < 7:
            return {
                'buttonPressed': 'yes'
            }
        mission_strategy = node['mission_strat'][player][perspective]
        fail_mission = bool(np.random.choice(len(vote_strategy), p=vote_strategy))
        return {
            'buttonPressed': 'no' if fail_mission else 'yes'
        }
    elif phase == 'assassination':
        assert node['type'] == 'TERMINAL_MERLIN'

        merlin_strat = node['merlin_strat'][player][perspective]

        p = np.random.choice(len(merlin_strat), p=merlin_strat)

        return {
            'buttonPressed': 'yes',
            'selectedPlayers': [ session_info['players'][p] ]
        }
    else:
        assert False, "Can't handle this case"
