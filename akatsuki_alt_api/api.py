from .utils import PaginatedQuery
from .objects import *
from .enums import *

import urllib.request
import urllib.error
import json
import time


class APIv1:

    def __init__(self, url = "https://akatalt.lekuru.xyz", delay=60/120):
        self.url = url
        self._last_request = 0
        self._delay = delay
    
    def _request(self, url: str) -> dict:
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
        self._last_request = time.time()
        try:
            with urllib.request.urlopen(req) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise e

    class ScoresQuery(PaginatedQuery[List[Score]]):
        
        def __init__(self, _api, query: str = "", length: int = 100, sort: ScoreSort = ScoreSort.PP, desc: bool = True):
            self._length = length
            self.count = 0
            self._api = _api
            self._sort = sort
            self._desc = desc
            super().__init__(query)

        def execute(self) -> List[Score]:
            data = self._api._request(f"{self._api.url}/api/v1/score/search?query={self.query}&page={self._page}&length={self._length}&sort={self._sort}&desc={self._desc}")
            if data:
                self.count = data['count']
                return [Score(**s) for s in data['scores']]
            else:
                return []

        def set_sort(self, sort: ScoreSort = ScoreSort.PP, desc: bool = True):
            self._sort = sort
            self._desc = desc
            self._page = 1

    def get_user(self, server: str, id: int) -> User:
        data = self._request(f"{self.url}/api/v1/user?server={server}&id={id}")
        return User(**data) if data else None

    def get_user_list(self, server: str, page: int = 1, length: int = 100, query: str = "", sort: UserSort = UserSort.LATEST_ACTIVITY, desc: bool = True) -> Tuple[List[User], int]:
        data = self._request(f"{self.url}/api/v1/user/list?server={server}&query={query}&page={page}&length={length}&sort={sort}&desc={desc}")
        return [User(**u) for u in data['users']], data['count']

    def get_beatmap(self, beatmap_id: int) -> Beatmap | None:
        data = self._request(f"{self.url}/api/v1/beatmap/{beatmap_id}")
        return Beatmap(**data) if data else None
    
    def get_beatmapset(self, beatmapset_id: int) -> Beatmapset | None:
        data = self._request(f"{self.url}/api/v1/beatmapset/{beatmapset_id}")
        return Beatmapset(**data) if data else None

    def get_score(self, server: str, score_id: int) -> Score | None:
        data = self._request(f"{self.url}/api/v1/score?server={server}&id={score_id}")
        return Score(**data) if data else None

    def get_scores(self, query: str, page: int = 1, length: int = 100, sort: str = ScoreSort.PP, desc: bool = True) -> Tuple[List[Score], int]:
        data = self._request(f"{self.url}/api/v1/score/search?query={query}&page={page}&length={length}&sort={sort}&desc={desc}")
        return [Score(**s) for s in data['scores']], data['count'] if data else [], 0

    def query_scores(self, query: str = "", length: int = 100, sort: str = ScoreSort.PP, desc: bool = True) -> ScoresQuery:
        return self.ScoresQuery(self, query, length, sort, desc)

instance = APIv1()
