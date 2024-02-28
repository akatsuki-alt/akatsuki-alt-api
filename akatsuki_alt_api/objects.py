from datetime import datetime
from typing import List

class Model:

    _cast_func = {}
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in self._cast_func:
                v = self._cast_func[k](v)
            setattr(self, k, v)

class User(Model):
    _cast_func = {'latest_activity': datetime.fromisoformat, 'registered_on': datetime.fromisoformat}

    id: int
    clan_id: int
    server: str
    username: str
    username_history: List[str]
    country: str
    registered_on: datetime
    latest_activity: datetime
    favourite_mode: int
    banned: bool
    is_bot: bool
    extra_metadata: dict
