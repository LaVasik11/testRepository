import time
from pprint import pprint
import random
import math

TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {
    "offset": 0,
    "score": {
        "home": 0,
        "away": 0
    }
}


def generate_stamp(previous_value):
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = 1 if score_changed and random.random() > 1 - \
        PROBABILITY_HOME_SCORE else 0
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change
        }
    }


def generate_game():
    stamps = [INITIAL_STAMP, ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


game_stamps = generate_game()

pprint(game_stamps)


def get_score(game_stamps: list[dict], offset: int) -> dict:
    """
    Возвращает состояние счета на момент времени offset.
    Если offset меньше или равен первой метке времени в списке, возвращается начальное состояние счета.
    """
    low = 0
    high = len(game_stamps) - 1

    if offset <= game_stamps[0]["offset"]:
        return game_stamps[0]["score"]

    while low <= high:
        mid = (low + high) // 2
        if game_stamps[mid]["offset"] == offset:
            return game_stamps[mid]["score"]
        elif game_stamps[mid]["offset"] < offset:
            low = mid + 1
        else:
            high = mid - 1

    return game_stamps[high]["score"]


offset = 10000
score_at_offset = get_score(game_stamps, offset)
print("Score at offset", offset, ":", score_at_offset)
