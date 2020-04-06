import random

ranks = ("A","2","3","4","5","6","7","8","9","T","J","Q","K")
suits = ("s","h","d","c")

def rank(c):
    if len(c) != 2:
        raise ValueError(f"invalid card {c}")
    r = c[0]
    if r not in ranks:
        raise ValueError(f"invalid card {c}")
    return r

def suit(c):
    if len(c) != 2:
        raise ValueError(f"invalid card {c}")
    s = c[1]
    if s not in suits:
        raise ValueError(f"invalid card {c}")
    return s

def deck():
    d = [r+s for r in ranks for s in suits]
    random.shuffle(d)
    return d

def pointValue(card):
    r = rank(card)
    if r == "A":
        return 1
    elif r in ("T","J","Q","K"):
        return 10
    else:
        return int(r)