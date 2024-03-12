from enum import StrEnum

class UserSort(StrEnum):
    
    USER_ID = "id"
    CLAN_ID = "clan_id"
    USERNAME = "username"
    LATEST_ACTIVITY = "latest_activity"
    REGISTERED_ON = "registered_on"
    COUNTRY = "country"

class ScoreSort(StrEnum):
    
    SCORE_ID = "id"
    USER_ID = "user_id"
    BEATMAP_ID = "beatmap_id"
    MAX_COMBO = "max_combo"
    ACCURACY = "accuracy"
    PP = "pp"
    SCORE = "score"
    MODS = "mods"
    DATE = "date"

class BeatmapSort(StrEnum):
    
    BEATMAP_ID = "id"
    BEATMAPSET_ID = "set_id"
    MAX_COMBO = "max_combo"
    BPM = "bpm"
    TOTAL_LENGTH = "total_length"
    HIT_LENGTH = "hit_length"
    DIFFICULTY = "difficulty"

class FirstPlacesType(StrEnum):
    
    ALL = "all"
    NEW = "new"
    LOST = "lost"
