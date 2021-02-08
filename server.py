from flask import Flask, request, jsonify
from functools import wraps
import time

app = Flask(__name__)
limits = {}


def limit_request(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        client_id = request.args.get('clientId')
        if not verify_limits(client_id):
            return "Service Unavailable: ClientId={} is temporary blocked".format(client_id), 503
        return f(*args, **kwargs)
    return wrap


def verify_limits(client_id):
    now = time.time()

    # New client, start a new time frame
    if client_id not in limits.keys():
        limits[client_id] = {
            'first_call': now,
            'count': 1
        }
        return True

    first_call = limits[client_id]['first_call']
    count = limits[client_id]['count']

    # Allow 5 requests in 5 seconds time frame
    if (now - first_call) < 5 and count <= 5:
        limits[client_id]['count'] += 1
        return True

    # Time frame expires after 5 seconds of first call, should be restarted
    if (now - first_call) >= 5:
        limits[client_id] = {
            'first_call': now,
            'count': 1
        }
        return True

    # Otherwise should be rejected
    return False


@app.route('/')
@limit_request
def index():
    client_id = request.args.get('clientId')
    print("Request from clientId={} allowed".format(client_id))
    return '', 200
