import os
import websocket
import json

from slack import post_slack, slack_event

EVENT_TYPES = ["stack", "service", "container", "node_cluster", "node", "action"]

def on_error(ws, error):
    if VERBOSE:
        print error
 
def on_close(ws):
    r = post_slack("Tutum Stream connection closed.")
    if VERBOSE:
        print "### closed ###"
 
def on_message(ws, message):
    msg_as_JSON = json.loads(message)
    type = msg_as_JSON.get("type")
    state = msg_as_JSON.get("state").lower()
    if type:
        if type == "auth":
            if VERBOSE:
                print "Auth completed"
        elif state in CONF[type]:
            print 'sending....'
            resource_uri = msg_as_JSON.get("resource_uri")
            r = slack_event(type, state, resource_uri)
            print r.status_code
            if VERBOSE:
                print message
        elif state not in CONF[type]:
            if VERBOSE:
                print message
 
def on_open(ws):
    r = post_slack("Tutum Stream connection open.")
    if VERBOSE:
        print "Connected"

def get_config():
    conf = {}
    for type in EVENT_TYPES:
        states = os.environ.get(type.upper(), '')
        conf[type] = [state.strip() for state in states.lower().split(',')]
    return conf
 
if __name__ == "__main__":
    websocket.enableTrace(False)
    token = os.environ.get('TUTUM_TOKEN')
    username = os.environ.get('TUTUM_USERNAME')
    TUTUM_AUTH = os.environ.get('TUTUM_AUTH')
    VERBOSE = (os.environ.get('VERBOSE', True))
    if VERBOSE == "False":
        VERBOSE = False

    CONF = get_config()

    if TUTUM_AUTH:
        TUTUM_AUTH = TUTUM_AUTH.replace(' ', '%20')
        url = 'wss://stream.tutum.co/v1/events?auth={}'.format(TUTUM_AUTH)
    elif token and username:
        url = 'wss://stream.tutum.co/v1/events?token={}&user={}'.format(token, username)
    else:
        raise Exception("Please provide authentication credentials")

    ws = websocket.WebSocketApp(url, 
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                on_open = on_open)
 
    try:
        ws.run_forever()
    except KeyboardInterrupt:
        pass
