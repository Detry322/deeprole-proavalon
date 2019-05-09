import requests
import json

BASE_URL = 'http://127.0.0.1:5000/deeprole'

def make_request(endpoint, data, method='POST'):
    HEADERS = {}

    if data is not None:
        HEADERS['Content-Type'] = 'application/json'
        data = json.dumps(data)

    if method == 'GET':
        r = requests.get('{}{}'.format(BASE_URL, endpoint), headers=HEADERS, data=data)
    else:
        r = requests.post('{}{}'.format(BASE_URL, endpoint), headers=HEADERS, data=data)

    return r.json()


# Create a session
print("---- Creating session")
response = make_request('/v0/session', {
    'numPlayers': 5,
    'roles': ['Assassin', 'Spy', 'Resistance', 'Merlin'],
    'cards': [],
    'teamLeader': 1,
    'players': ["detry322","Bot1","Bot0","Bot3","Bot2"],
    'name': 'detry322',
    'role': 'Resistance'
})
assert 'sessionID' in response, response
session_id = response['sessionID']
print("Session created:", session_id)

print("Action 1 of 7")
# Succeeds: 0, Fails: 0, Propose: 0, Request an action - approve or reject Bot1's proposal
response = make_request('/v0/session/act', {
    'sessionID': session_id,
    'gameInfo': {"alliance":"Resistance","role":"Resistance","username":"detry322","buttons":{"green":{"hidden":False,"disabled":False,"setText":"Approve"},"red":{"hidden":False,"disabled":False,"setText":"Reject"}},"statusMessage":"Bot1 has picked: Bot3, Bot2.","missionNum":1,"missionHistory":[],"numFailsHistory":[],"pickNum":1,"teamLeader":1,"hammer":0,"playersYetToVote":["detry322","Bot1","Bot0","Bot3","Bot2"],"phase":"votingTeam","proposedTeam":["Bot3","Bot2"],"numPlayersOnMission":["2","3","2","3","3"],"numSelectTargets":None,"votes":[],"voteHistory":{"detry322":[[""]],"Bot2":[["VHpicked "]],"Bot3":[["VHpicked "]],"Bot0":[[""]],"Bot1":[["VHleader "]]},"winner":"","spectator":False,"gamePlayersInRoom":["detry322","Bot1","Bot0","Bot3","Bot2"],"roomId":101,"toShowGuns":True,"publicData":{"roles":{},"cards":{}}}
})
assert response.get('buttonPressed') in ['yes', 'no'], response

print("Action 2 of 7")
# Everyone approves the mission. The mission passes. It's Bot0's turn to propose. He proposes detry322, Bot3, and Bot2
# Succeeds: 1, Fails: 0, Propose: 0, Request an action - approve or reject Bot0's proposal
response = make_request('/v0/session/act', {
    'sessionID': session_id,
    'gameInfo': {"alliance":"Resistance","role":"Resistance","username":"detry322","buttons":{"green":{"hidden":False,"disabled":False,"setText":"Approve"},"red":{"hidden":False,"disabled":False,"setText":"Reject"}},"statusMessage":"Bot0 has picked: detry322, Bot2, Bot3.","missionNum":2,"missionHistory":["succeeded"],"numFailsHistory":[0],"pickNum":1,"teamLeader":2,"hammer":1,"playersYetToVote":["detry322","Bot1","Bot0","Bot3","Bot2"],"phase":"votingTeam","proposedTeam":["detry322","Bot2","Bot3"],"numPlayersOnMission":["2","3","2","3","3"],"numSelectTargets":None,"votes":[],"voteHistory":{"detry322":[["VHapprove"],["VHpicked "]],"Bot2":[["VHpicked VHapprove"],["VHpicked "]],"Bot3":[["VHpicked VHapprove"],["VHpicked "]],"Bot0":[["VHapprove"],["VHleader "]],"Bot1":[["VHleader VHapprove"],[""]]},"winner":"","spectator":False,"gamePlayersInRoom":["detry322","Bot1","Bot0","Bot3","Bot2"],"roomId":101,"toShowGuns":True,"publicData":{"roles":{},"cards":{}}}
})
assert response.get('buttonPressed') in ['yes', 'no'], response

print("Action 3 of 7")
# The proposal is voted down by detry322, bot1, and bot3. It's Bot3's turn. He proposes detry322, Bot0 and Bot3
# Succeeds: 1, Fails: 0, Propose: 1, Request an action - approve or reject Bot3's proposal
response = make_request('/v0/session/act', {
    'sessionID': session_id,
    'gameInfo': {"alliance":"Resistance","role":"Resistance","username":"detry322","buttons":{"green":{"hidden":False,"disabled":False,"setText":"Approve"},"red":{"hidden":False,"disabled":False,"setText":"Reject"}},"statusMessage":"Bot3 has picked: Bot0, detry322, Bot3.","missionNum":2,"missionHistory":["succeeded"],"numFailsHistory":[0],"pickNum":2,"teamLeader":3,"hammer":1,"playersYetToVote":["detry322","Bot1","Bot0","Bot3","Bot2"],"phase":"votingTeam","proposedTeam":["Bot0","detry322","Bot3"],"numPlayersOnMission":["2","3","2","3","3"],"numSelectTargets":None,"votes":[],"voteHistory":{"detry322":[["VHapprove"],["VHpicked VHreject","VHpicked "]],"Bot2":[["VHpicked VHapprove"],["VHpicked VHapprove",""]],"Bot3":[["VHpicked VHapprove"],["VHpicked VHreject","VHpicked VHleader "]],"Bot0":[["VHapprove"],["VHleader VHapprove","VHpicked "]],"Bot1":[["VHleader VHapprove"],["VHreject",""]]},"winner":"","spectator":False,"gamePlayersInRoom":["detry322","Bot1","Bot0","Bot3","Bot2"],"roomId":101,"toShowGuns":True,"publicData":{"roles":{},"cards":{}}}
})
assert response.get('buttonPressed') in ['yes', 'no'], response


print("Action 4 of 7")
# The proposal is approved. The mission passes. It's Bot2's turn. He proposes Bot1 and Bot0.
# Succeeds: 2, Fails: 0, Propose: 0. Request an action - approve or reject Bot2's proposal
response = make_request('/v0/session/act', {
    'sessionID': session_id,
    'gameInfo': {"alliance":"Resistance","role":"Resistance","username":"detry322","buttons":{"green":{"hidden":False,"disabled":False,"setText":"Approve"},"red":{"hidden":False,"disabled":False,"setText":"Reject"}},"statusMessage":"Bot2 has picked: Bot1, Bot0.","missionNum":3,"missionHistory":["succeeded","succeeded"],"numFailsHistory":[0,0],"pickNum":1,"teamLeader":4,"hammer":3,"playersYetToVote":["detry322","Bot1","Bot0","Bot3","Bot2"],"phase":"votingTeam","proposedTeam":["Bot1","Bot0"],"numPlayersOnMission":["2","3","2","3","3"],"numSelectTargets":None,"votes":[],"voteHistory":{"detry322":[["VHapprove"],["VHpicked VHreject","VHpicked VHapprove"],[""]],"Bot2":[["VHpicked VHapprove"],["VHpicked VHapprove","VHapprove"],["VHleader "]],"Bot3":[["VHpicked VHapprove"],["VHpicked VHreject","VHpicked VHleader VHreject"],[""]],"Bot0":[["VHapprove"],["VHleader VHapprove","VHpicked VHreject"],["VHpicked "]],"Bot1":[["VHleader VHapprove"],["VHreject","VHapprove"],["VHpicked "]]},"winner":"","spectator":False,"gamePlayersInRoom":["detry322","Bot1","Bot0","Bot3","Bot2"],"roomId":101,"toShowGuns":True,"publicData":{"roles":{},"cards":{}}}
})
assert response.get('buttonPressed') in ['yes', 'no'], response

print("Action 5 of 7")
# The proposal is approved. The mission fails. It's detry322's turn.
# Succeeds: 2, Fails: 1, Propose: 0. Request an action - propose someone!
response = make_request('/v0/session/act', {
    'sessionID': session_id,
    'gameInfo': {"alliance":"Resistance","role":"Resistance","username":"detry322","buttons":{"green":{"hidden":False,"disabled":True,"setText":"Pick"},"red":{"hidden":True,"disabled":True,"setText":""}},"statusMessage":"Your turn to pick a team. Pick 3 players.","missionNum":4,"missionHistory":["succeeded","succeeded","failed"],"numFailsHistory":[0,0,1],"pickNum":1,"teamLeader":0,"hammer":4,"playersYetToVote":[],"phase":"pickingTeam","proposedTeam":[],"numPlayersOnMission":["2","3","2","3","3"],"numSelectTargets":3,"votes":["approve","reject","approve","approve","approve"],"voteHistory":{"detry322":[["VHapprove"],["VHpicked VHreject","VHpicked VHapprove"],["VHapprove"]],"Bot2":[["VHpicked VHapprove"],["VHpicked VHapprove","VHapprove"],["VHleader VHreject"]],"Bot3":[["VHpicked VHapprove"],["VHpicked VHreject","VHpicked VHleader VHreject"],["VHapprove"]],"Bot0":[["VHapprove"],["VHleader VHapprove","VHpicked VHreject"],["VHpicked VHapprove"]],"Bot1":[["VHleader VHapprove"],["VHreject","VHapprove"],["VHpicked VHapprove"]]},"winner":"","spectator":False,"gamePlayersInRoom":["detry322","Bot1","Bot0","Bot3","Bot2"],"roomId":101,"toShowGuns":False,"publicData":{"roles":{},"cards":{}}}
})
assert response.get('buttonPressed') == 'yes', response
assert len(response.get('selectedPlayers', [])) == 3, response
assert set(response.get('selectedPlayers', [])).issubset(set(["detry322","Bot1","Bot0","Bot3","Bot2"])), response

print("Action 6 of 7")
# You propose Bot1, Bot0, Bot3. Request an action - approve or reject your proposal!
response = make_request('/v0/session/act', {
    'sessionID': session_id,
    'gameInfo': {"alliance":"Resistance","role":"Resistance","username":"detry322","buttons":{"green":{"hidden":False,"disabled":False,"setText":"Approve"},"red":{"hidden":False,"disabled":False,"setText":"Reject"}},"statusMessage":"detry322 has picked: Bot3, Bot0, Bot1.","missionNum":4,"missionHistory":["succeeded","succeeded","failed"],"numFailsHistory":[0,0,1],"pickNum":1,"teamLeader":0,"hammer":4,"playersYetToVote":["detry322","Bot1","Bot0","Bot3","Bot2"],"phase":"votingTeam","proposedTeam":["Bot3","Bot0","Bot1"],"numPlayersOnMission":["2","3","2","3","3"],"numSelectTargets":None,"votes":[],"voteHistory":{"detry322":[["VHapprove"],["VHpicked VHreject","VHpicked VHapprove"],["VHapprove"],["VHleader "]],"Bot2":[["VHpicked VHapprove"],["VHpicked VHapprove","VHapprove"],["VHleader VHreject"],[""]],"Bot3":[["VHpicked VHapprove"],["VHpicked VHreject","VHpicked VHleader VHreject"],["VHapprove"],["VHpicked "]],"Bot0":[["VHapprove"],["VHleader VHapprove","VHpicked VHreject"],["VHpicked VHapprove"],["VHpicked "]],"Bot1":[["VHleader VHapprove"],["VHreject","VHapprove"],["VHpicked VHapprove"],["VHpicked "]]},"winner":"","spectator":False,"gamePlayersInRoom":["detry322","Bot1","Bot0","Bot3","Bot2"],"roomId":101,"toShowGuns":True,"publicData":{"roles":{},"cards":{}}}
})
assert response.get('buttonPressed') in ['yes', 'no'], response

print("Action 7 of 7")
# The mission fails. It's Bot1's turn to propose. They propose detry322, Bot1 and Bot2. 
# Succeeds: 2, Fails: 2, Propose: 0. Request an action - Approve or reject.
response = make_request('/v0/session/act', {
    'sessionID': session_id,
    'gameInfo': {"alliance":"Resistance","role":"Resistance","username":"detry322","buttons":{"green":{"hidden":False,"disabled":False,"setText":"Approve"},"red":{"hidden":False,"disabled":False,"setText":"Reject"}},"statusMessage":"Bot1 has picked: detry322, Bot1, Bot2.","missionNum":5,"missionHistory":["succeeded","succeeded","failed","failed"],"numFailsHistory":[0,0,1,1],"pickNum":1,"teamLeader":1,"hammer":0,"playersYetToVote":["detry322","Bot1","Bot0","Bot3","Bot2"],"phase":"votingTeam","proposedTeam":["detry322","Bot1","Bot2"],"numPlayersOnMission":["2","3","2","3","3"],"numSelectTargets":None,"votes":[],"voteHistory":{"detry322":[["VHapprove"],["VHpicked VHreject","VHpicked VHapprove"],["VHapprove"],["VHleader VHapprove"],["VHpicked "]],"Bot2":[["VHpicked VHapprove"],["VHpicked VHapprove","VHapprove"],["VHleader VHreject"],["VHapprove"],["VHpicked "]],"Bot3":[["VHpicked VHapprove"],["VHpicked VHreject","VHpicked VHleader VHreject"],["VHapprove"],["VHpicked VHreject"],[""]],"Bot0":[["VHapprove"],["VHleader VHapprove","VHpicked VHreject"],["VHpicked VHapprove"],["VHpicked VHapprove"],[""]],"Bot1":[["VHleader VHapprove"],["VHreject","VHapprove"],["VHpicked VHapprove"],["VHpicked VHreject"],["VHpicked VHleader "]]},"winner":"","spectator":False,"gamePlayersInRoom":["detry322","Bot1","Bot0","Bot3","Bot2"],"roomId":101,"toShowGuns":True,"publicData":{"roles":{},"cards":{}}}
})
assert response.get('buttonPressed') in ['yes', 'no'], response

print("Game over!")
response = make_request('/v0/session/gameover', {
    'sessionID': session_id,
    'gameInfo': {"alliance":"Resistance","role":"Resistance","see":{"spies":["Bot2","Bot0"],"roles":["Resistance","Assassin","Resistance","Spy","Merlin"]},"username":"detry322","buttons":{"green":{"hidden":True,"disabled":True,"setText":""},"red":{"hidden":True,"disabled":True,"setText":""}},"statusMessage":"Game has finished. The resistance have won.","missionNum":5,"missionHistory":["succeeded","succeeded","failed","failed","succeeded"],"numFailsHistory":[0,0,1,1,0],"pickNum":1,"teamLeader":1,"hammer":0,"playersYetToVote":[],"phase":"finished","proposedTeam":["detry322","Bot1","Bot2"],"numPlayersOnMission":["2","3","2","3","3"],"numSelectTargets":None,"votes":[],"voteHistory":{"detry322":[["VHapprove"],["VHpicked VHreject","VHpicked VHapprove"],["VHapprove"],["VHleader VHapprove"],["VHpicked VHapprove"]],"Bot2":[["VHpicked VHapprove"],["VHpicked VHapprove","VHapprove"],["VHleader VHreject"],["VHapprove"],["VHpicked VHapprove"]],"Bot3":[["VHpicked VHapprove"],["VHpicked VHreject","VHpicked VHleader VHreject"],["VHapprove"],["VHpicked VHreject"],["VHreject"]],"Bot0":[["VHapprove"],["VHleader VHapprove","VHpicked VHreject"],["VHpicked VHapprove"],["VHpicked VHapprove"],["VHapprove"]],"Bot1":[["VHleader VHapprove"],["VHreject","VHapprove"],["VHpicked VHapprove"],["VHpicked VHreject"],["VHpicked VHleader VHreject"]]},"winner":"Resistance","spectator":False,"gamePlayersInRoom":["detry322","Bot1","Bot0","Bot3","Bot2"],"roomId":101,"toShowGuns":True,"publicData":{"roles":{"assassinShotUsername":"detry322","assassinShotUsername2":""},"cards":{}}}
})
print("Done.")
