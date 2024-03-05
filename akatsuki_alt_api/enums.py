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
