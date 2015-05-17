import json
import os
import requests

SLACK_URL = os.environ.get('SLACK_URL', '')

def slack_event(type, action, resource_uri):
    text = ("You had a {0} event on Tutum!\n" 
            "Your {0}'s state is {1}.\n"
            "Check {2} to see more details.".format(type, action, resource_uri))
    return post_slack(text)

def post_slack(text):
    data = {"text": text}
    r = requests.post(SLACK_URL, data=json.dumps(data))
    return r
