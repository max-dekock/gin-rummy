from .card import *
from collections import defaultdict

def isRun(meld):
    if len(meld) < 3:
        return False
    bySuit = defaultdict(list)
    for card in meld:
        bySuit[suit(card)].append(rank(card))
    if len(bySuit.keys()) != 1:
        return False
    ri = [ranks.index(r) for r in bySuit[next(iter(bySuit.keys()))]]
    ri.sort()
    prev = None
    for i in ri:
        if prev is not None and i != prev + 1:
            return False
        prev = i
    return True

def isSet(meld):
    if len(meld) < 3:
        return False
    r = None
    for card in meld:
        if r is None:
            r = rank(card)
        elif rank(card) != r:
            return False
    return True

def isMeld(meld):
    # checking sets is faster than runs, so check those first
    return isSet(meld) or isRun(meld)