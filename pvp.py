import random

matches = {}

def create_match(u1, u2):
    mid = random.randint(1000, 9999)

    matches[mid] = {
        "players": [u1, u2],
        "scores": {u1: 0, u2: 0}
    }

    return mid


def add_score(mid, uid, score):
    if mid in matches:
        matches[mid]["scores"][uid] += score


def winner(mid):
    m = matches[mid]
    return max(m["scores"], key=m["scores"].get)
