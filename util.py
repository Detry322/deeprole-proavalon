import os
import functools
import hashlib
import json

from flask import request
from flask import current_app as app
from flask_api import exceptions

AUTH_KEY = os.environ.get('SECRET_AUTH_KEY')

def require_auth_decorator(f):
    @functools.wraps(f)
    def decorated_func(*args, **kwargs):
        if not app.debug and request.headers.get('Authorization') != AUTH_KEY:
            raise exceptions.AuthenticationFailed(detail="API Key Incorrect")
        return f(*args, **kwargs)
    return decorated_func


CAPABILITIES = [
    {
        "numPlayers": [5],
        "cards": [],
        "roles": ['Resistance', 'Spy', 'Assassin', 'Merlin']
    }
]


def matches_capabilities(session_create):
    for capability in CAPABILITIES:
        if session_create["numPlayers"] not in capability["numPlayers"]:
            continue
        if not set(session_create["roles"]).issubset(set(capability["roles"])):
            continue
        # # Hacky code since deeprole needs both merlin and assassin
        # if 'Assassin' not in session_create['roles'] or 'Merlin' not in session_create['roles']:
        #     continue
        if not set(session_create["cards"]).issubset(set(capability["cards"])):
            continue
        return True
    return False 


def get_missing_fields(obj, fields):
    return [field for field in fields if field not in obj.keys()]


def quickhash(data):
    h = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8'))
    return h.digest().hex()
