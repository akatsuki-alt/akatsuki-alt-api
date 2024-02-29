from .objects import *

import urllib.request
import urllib.error
import json
import time


class APIv1:

    def __init__(self, url = "https://akatalt.lekuru.xyz"):
        self.url = url
        self._last_request = 0
        self._delay = 60/120
    
    def _request(self, url: str) -> dict:
        global _last_request
        delta = time.time() - self._last_request
        if delta < self._delay:
            time.sleep(self._delay - delta)
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

    def get_user(self, server: str, id: int):
        data = self._request(f"{self.url}/api/v1/user?server={server}&id={id}")
        return User(**data)

    def get_beatmap(self, beatmap_id: int):
        data = self._request(f"{self.url}/api/v1/beatmap/{beatmap_id}")
        return Beatmap(**data)
    
    def get_beatmapset(self, beatmapset_id: int):
        data = self._request(f"{self.url}/api/v1/beatmapset/{beatmapset_id}")
        if data:
            return Beatmapset(**data)
    
instance = APIv1()