import random

WORDS = [
    "CAT","DOG","SUN","RUN","MAP","CUP","FOX","CAR","BOX","PEN","KEY",
    "ABLE","BACK","GAME","HAND","JUMP","KING","LIFE","MIND","NOTE","ROAD",
    "BLAZE","CLOUD","DREAM","FLAME","GRACE","HEART","MAGNET","ORACLE","SHADOW"
]

class WordGridGame:
    def __init__(self, diff="easy"):
        self.words = random.sample(WORDS, 10)
        self.found = []
        self.score = 0
        self.streak = 0

    def check_word(self, w):
        w = w.upper()
        return w in self.words and w not in self.found

    def add_score(self, w):
        w = w.upper()
        self.found.append(w)

        base = 5
        bonus = 5 if len(w) >= 6 else 0
        self.score += base + bonus
        return base + bonus
