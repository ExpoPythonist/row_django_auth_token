#!/usr/bin/python3

import http.client
import json

from alchem import AUTH0_DOMAIN, API_AUDIENCE, ALGORITHMS
from alchem import CLIENT_SECRET

def get_access_token():
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    
    payload = "{\"client_id\":\"5Npc6DrAwLXhXxz9N39JVTe0Y168lXvq\",\"client_secret\":\"%s\",\"audience\":\"%s\",\"grant_type\":\"client_credentials\"}" % (CLIENT_SECRET, API_AUDIENCE)
    headers = {'content-type': "application/json"}
    
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    s = data.decode("utf-8")
    d = json.loads(s)
    token_type = d['token_type']
    access_token = d['access_token']
    
    return token_type, access_token