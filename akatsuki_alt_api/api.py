from .objects import *

import urllib.request
import urllib.error
import json
import time

_last_request = 0
_delay = 60/120

def _request(url: str) -> dict:
    global _last_request
    delta = time.time() - _last_request
    if delta < _delay:
        time.sleep(_delay - delta)
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Akatsuki! Alt API Wrapper (python)'
        }
    )
    _last_request = time.time()
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise e

class APIv1:

    def __init__(self, url = "https://akatalt.lekuru.xyz"):
        self.url = url

    def get_user(self, server: str, id: int):
        data = _request(f"{self.url}/api/v1/user?server={server}&id={id}")
        return User(**data)

instance = APIv1()