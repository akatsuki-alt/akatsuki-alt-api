from typing import List, Dict, Tuple
from datetime import datetime

parse_date = datetime.fromisoformat

def _parse_set(beatmapset):
    return Beatmapset(**beatmapset)

def _parse_beatmap(beatmap):
    return Beatmap(**beatmap)

def _parse_beatmaps(beatmaps):
    return [Beatmap(**b) for b in beatmaps]

class Model:

    _cast_func = {}
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in self._cast_func:
                v = self._cast_func[k](v)
            setattr(self, k, v)
    def __repr__(self) -> str:
        string = f"{self.__class__.__name__}:\n"
        for k,v in self.__dict__.items():
            string += f"{k}: {v}\n"
        return string
class User(Model):

    _cast_func = {'latest_activity': parse_date, 'registered_on': parse_date}

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

class Beatmap(Model):
    
    _cast_func = {'last_update': parse_date, 'last_db_update': parse_date, 'beatmapset': _parse_set}
    
    id: int
    set_id: int
    mode: int
    md5: str
    version: str
    last_update: datetime
    max_combo: int
    bpm: float
    cs: float
    od: float
    ar: float
    hp: float
    diff: float
    hit_length: int
    total_length: int
    count_circles: int
    count_sliders: int
    count_spinners: int
    status: Dict[str, int]
    last_db_update: datetime

class Beatmapset(Model):

    _cast_func = {'last_updated': parse_date, 'ranked_date': parse_date, 'submitted_date': parse_date, 'beatmaps': _parse_beatmaps}
    
    id: int
    artist: str
    artist_unicode: str
    title: str
    title_unicode: str
    source: str
    mapper: str
    nominators: Dict[str, List[str]]
    tags: List[str]
    pack_tags: List[str]
    genre: str
    language: str
    nsfw: bool
    video: bool
    spotlight: bool
    availability: bool

    last_updated: datetime
    ranked_date: datetime
    submitted_date: datetime

    beatmaps: List[Beatmap]

class Score(Model):
    
    _cast_func = {'date': parse_date, 'last_updated': parse_date, 'beatmap': _parse_beatmap}

    id: int
    user_id: int
    server: str
    beatmap_id: int
    beatmap_md5: str
    max_combo: int
    full_combo: bool
    count_300: int
    count_100: int
    count_50: int
    count_miss: int
    count_katu: int
    count_geki: int
    accuracy: float
    rank: str
    pp: float
    score: int
    mods: int
    mods_relax: dict | None
    mode: int
    relax: int
    completed: int
    date: datetime
    
    hidden: bool
    pp_system: str
    last_updated: datetime
    extra_metadata: dict

    beatmap: Beatmap
