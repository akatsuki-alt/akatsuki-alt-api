from .enums import ScoreSort
from .utils import PaginatedQuery
from .objects import *
from .enums import *

from datetime import date

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
            self._page = 0

    class FirstPlacesQuery(ScoresQuery):
        
        def __init__(self, _api, server: str, user_id: int, mode = 0, relax = 0, date: date = None, query: str = "", length: int = 100, sort: ScoreSort = ScoreSort.PP, desc: bool = True):
            self._server = server
            self._user_id = user_id
            self._date = date
            self._mode = mode
            self._relax = relax
            super().__init__(_api, query, length, sort, desc)
        
        def execute(self) -> List[Score]:
            url = f"{self._api.url}/api/v1/user/first_places?server={self._server}&id={self._user_id}&mode={self._mode}&relax={self._relax}&page={self._page}&length={self._length}&query={self.query}&sort={self._sort}&desc={self._desc}"
            if self._date:
                url += f"&date={self._date}"
            data = self._api._request(url)
            if data or data['count']:
                self.count = data['count']
                return [Score(**score) for score in data['scores']]
            return []

    class UsersQuery(PaginatedQuery[List[User]]):
        
        def __init__(self, _api, server: str, query: str = "", length: int = 100, sort: UserSort = UserSort.LATEST_ACTIVITY, desc: bool = True):
            self._length = length
            self.count = 0
            self._api = _api
            self._sort = sort
            self._desc = desc
            self.server = server
            super().__init__(query)

        def execute(self) -> List[User]:
            data = self._api._request(f"{self._api.url}/api/v1/user/list?server={self.server}&query={self.query}&page={self._page}&length={self._length}&sort={self._sort}&desc={self._desc}")
            if data:
                self.count = data['count']
                return [User(**s) for s in data['users']]
            else:
                return []

        def set_sort(self, sort: UserSort = UserSort.LATEST_ACTIVITY, desc: bool = True):
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

    def get_user_first_places(self, server: str, user_id: int, mode: int = 0, relax: int = 0, page: int = 1, length: int = 100, date: date = None, query: str = "", sort: str = ScoreSort.PP, desc: bool = True) -> Tuple[List[Score], int]:
        url = f"{self.url}/api/v1/user/first_places?server={server}&id={user_id}&mode={mode}&relax={relax}&page={page}&length={length}&query={query}&sort={sort}&desc={desc}"
        if date:
            url += f"&date={date}"
        data = self._request(url)
        if data or data['count']:
            return [Score(**score) for score in data['scores']], data['count']
        return [], 0

    def lookup_first_place(self, server: str, beatmap_id: int, mode: int = 0, relax: int = 0, date: date = None) -> FirstPlace | None:
        url = f"{self.url}/api/v1/user/first_places/lookup?server={server}&beatmap_id={beatmap_id}&mode={mode}&relax={relax}"
        if date:
            url += f"&date={date}"
        data = self._request(url)
        return FirstPlace(**data) if data else None

    def get_first_place_history(self, server: str, beatmap_id: int, mode: int = 0, relax: int = 0, page: int = 1, length: int = 100) -> Tuple[List[FirstPlace], int]:
        data = self._request(f"{self.url}/api/v1/user/first_places/history/?server={server}&beatmap_id={beatmap_id}&mode={mode}&relax={relax}&page={page}&length={length}")
        if data:
            return [FirstPlace(**first_place) for first_place in data['history']], data['count']
        return [], 0

    def query_scores(self, query: str = "", length: int = 100, sort: ScoreSort = ScoreSort.PP, desc: bool = True) -> ScoresQuery:
        return self.ScoresQuery(self, query, length, sort, desc)

    def query_users(self, server: str, query: str = "", length: int = 100, sort: UserSort = UserSort.LATEST_ACTIVITY, desc: bool = True) -> UsersQuery:
        return self.UsersQuery(self, server, query, length, sort, desc)

    def query_user_first_places(self, server: str, user_id: int, mode: int = 0, relax: int = 0, query: str = "", length: int = 100, sort: ScoreSort = ScoreSort.PP, desc: bool = True, date: date = None) -> FirstPlacesQuery:
        return self.FirstPlacesQuery(self, server, user_id, mode, relax, date, query, length, sort, desc)

instance = APIv1()
