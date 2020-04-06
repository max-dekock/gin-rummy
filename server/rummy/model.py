from .card import *

class Rummy:
    scoring_defaults = {
        "gin": 20,
        "undercut": 10,
    }

    def __init__(self, player1, player2, **kwargs):
        self.players = (player1, player2)

        self.piles = {"stock": [], "discard": []}
        if "deck" in kwargs:
            self.piles["stock"] = kwargs["deck"]
        else:
            self.piles["stock"] = deck()
        self.hands = {player:[] for player in self.players}

        if "firstplayer" in kwargs:
            self.currentplayer = kwargs["firstplayer"]
        else:
            self.currentplayer = player1
        self.phase = "draw"

        self.scoring = dict(Rummy.scoring_defaults)
        if "scoring" in kwargs:
            self.scoring.update(kwargs["scoring"])

    def deal(self):
        stock = self.piles["stock"]
        for i in range(10):
            for player in self.players:
                self.hands[player].append(stock.pop())
        self.piles["discard"].append(stock.pop())

    def opponent(self, player):
        if player not in self.players:
            raise ValueError("invalid player")
        else:
            return self.players[self.players.index(player) - 1]

    def draw(self, player, pile):
        if player != self.currentplayer:
            raise Exception("wait your turn")
        if self.phase != "draw":
            raise Exception("wrong phase")
        draw = self.piles[pile].pop()
        self.hands[player].append(draw)
        self.phase = "discard"
        return draw

    def discard(self, player, card):
        if player != self.currentplayer:
            raise Exception("wait your turn")
        if self.phase != "discard":
            raise Exception("wrong phase")
        if card not in self.hands[player]:
            raise ValueError(f"card {card} not in player {player}'s hand")
        self.hands[player].remove(card)
        self.piles["discard"].append(card)
        self.currentplayer = self.opponent(self.currentplayer)
        self.phase = "draw"
        return card

    def top_discard(self):
        if len(self.piles["discard"]) > 0:
            return self.piles["discard"][-1]
        else:
            return None
