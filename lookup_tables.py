import itertools

hidden_state_to_assignment_id = {}

assignment_id_to_hidden_state = []

for i, (merlin, assassin, minion) in enumerate(itertools.permutations(range(5), 3)):
    hidden_state = ['Resistance']*5
    hidden_state[merlin] = 'Merlin'
    hidden_state[assassin] = 'Assassin'
    hidden_state[minion] = 'Spy'
    hidden_state_to_assignment_id[tuple(hidden_state)] = i
    assignment_id_to_hidden_state.append(tuple(hidden_state))


def get_deeprole_perspective(player, role, spies):
    if role == 'Resistance':
        return 0
    
    hidden_state = ['Resistance']*5

    buddy = list(set(spies) - set([player]))[0]

    if role == 'Spy':
        hidden_state[player] = 'Spy'
        hidden_state[buddy] = 'Assassin'
        hidden_state[hidden_state.index('Resistance')] = 'Merlin'
    elif role == 'Assassin':
        hidden_state[player] = 'Assassin'
        hidden_state[buddy] = 'Spy'
        hidden_state[hidden_state.index('Resistance')] = 'Merlin'
    elif role == 'Merlin':
        hidden_state[player] = 'Merlin'
        hidden_state[spies[0]] = 'Assassin'
        hidden_state[spies[1]] = 'Spy'

    assignemnt_id = hidden_state_to_assignment_id[tuple(hidden_state)]
    return ASSIGNMENT_TO_VIEWPOINT[assignemnt_id][player]


ASSIGNMENT_TO_VIEWPOINT = [
    [  1,    8,   12,    0,    0 ],
    [  2,    9,    0,   12,    0 ],
    [  3,   10,    0,    0,   12 ],
    [  1,   12,    8,    0,    0 ],
    [  4,    0,    9,   13,    0 ],
    [  5,    0,   10,    0,   13 ],
    [  2,   13,    0,    8,    0 ],
    [  4,    0,   13,    9,    0 ],
    [  6,    0,    0,   10,   14 ],
    [  3,   14,    0,    0,    8 ],
    [  5,    0,   14,    0,    9 ],
    [  6,    0,    0,   14,   10 ],
    [  8,    1,   11,    0,    0 ],
    [  9,    2,    0,   11,    0 ],
    [ 10,    3,    0,    0,   11 ],
    [ 12,    1,    7,    0,    0 ],
    [  0,    4,    9,   13,    0 ],
    [  0,    5,   10,    0,   13 ],
    [ 13,    2,    0,    7,    0 ],
    [  0,    4,   13,    9,    0 ],
    [  0,    6,    0,   10,   14 ],
    [ 14,    3,    0,    0,    7 ],
    [  0,    5,   14,    0,    9 ],
    [  0,    6,    0,   14,   10 ],
    [  7,   11,    1,    0,    0 ],
    [  9,    0,    2,   11,    0 ],
    [ 10,    0,    3,    0,   11 ],
    [ 11,    7,    1,    0,    0 ],
    [  0,    9,    4,   12,    0 ],
    [  0,   10,    5,    0,   12 ],
    [ 13,    0,    2,    7,    0 ],
    [  0,   13,    4,    8,    0 ],
    [  0,    0,    6,   10,   14 ],
    [ 14,    0,    3,    0,    7 ],
    [  0,   14,    5,    0,    8 ],
    [  0,    0,    6,   14,   10 ],
    [  7,   11,    0,    1,    0 ],
    [  8,    0,   11,    2,    0 ],
    [ 10,    0,    0,    3,   11 ],
    [ 11,    7,    0,    1,    0 ],
    [  0,    8,   12,    4,    0 ],
    [  0,   10,    0,    5,   12 ],
    [ 12,    0,    7,    2,    0 ],
    [  0,   12,    8,    4,    0 ],
    [  0,    0,   10,    6,   13 ],
    [ 14,    0,    0,    3,    7 ],
    [  0,   14,    0,    5,    8 ],
    [  0,    0,   14,    6,    9 ],
    [  7,   11,    0,    0,    1 ],
    [  8,    0,   11,    0,    2 ],
    [  9,    0,    0,   11,    3 ],
    [ 11,    7,    0,    0,    1 ],
    [  0,    8,   12,    0,    4 ],
    [  0,    9,    0,   12,    5 ],
    [ 12,    0,    7,    0,    2 ],
    [  0,   12,    8,    0,    4 ],
    [  0,    0,    9,   13,    6 ],
    [ 13,    0,    0,    7,    3 ],
    [  0,   13,    0,    8,    5 ],
    [  0,    0,   13,    9,    6 ]
]
