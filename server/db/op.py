import redis
import json
import os
import base64

from ..rummy import card
from ..rummy.melds import isMeld

scriptDir = os.path.dirname(__file__)

def loadScript(script, client):
    file = open(os.path.join(scriptDir, script))
    scriptContents = file.read(1000000) #no scripts > 1MB
    return client.register_script(scriptContents)

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r = redis.from_url(redis_url)

def gameKey(gameID):
    return f"game:{gameID}"

def playerKey(playerID):
    return f"player:{playerID}"

def newGame():
    with r.pipeline() as pipe:
        while True:
            try:
                gameID = str(base64.urlsafe_b64encode(os.urandom(6)), 'utf-8')
                key = gameKey(gameID)
                pipe.watch(key)
                if pipe.exists(key):
                    continue
                playerIDs = [str(base64.urlsafe_b64encode(os.urandom(6)), 'utf-8') for i in range(2)]
                opponents = {playerIDs[0]:playerIDs[1], playerIDs[1]:playerIDs[0]}
                players = { playerID: {
                                'ready': False,
                                'opponent': opponents[playerID]
                            } for playerID in playerIDs }
                pipe.multi()
                pipe.set(key, json.dumps({'started': False, 'players': players}))
                pipe.execute()
                break
            except redis.WatchError:
                continue
    return gameID, playerIDs

def joinCode(gameID, playerID):
    with r.pipeline() as pipe:
        while True:
            try:
                jc = str(base64.urlsafe_b64encode(os.urandom(6)), 'utf-8')
                key = f'joinCode:{jc}'
                pipe.watch(key)
                if pipe.exists(key):
                    continue
                pipe.multi()
                pipe.set(key, json.dumps({'gameID': gameID, 'playerID': playerID}))
                pipe.execute()
                break
            except redis.WatchError:
                continue
    return jc
                
def joinDecode(code):
    return json.loads(r.get(f'joinCode:{code}'))

def loadGameState(gameID):
    data = r.get(gameKey(gameID)).decode("utf-8")
    return json.loads(data)

joinGameScript = loadScript("joinGame.lua", r)
def joinGame(gameID, playerID, nickname):
    data = joinGameScript(keys=[gameKey(gameID)], args=[gameID, playerID, nickname])
    return json.loads(data)

startGameScript = loadScript("startGame.lua", r)
def startGame(gameID, startingPlayer):
    deck = "".join(card.deck())
    return startGameScript(keys=[gameKey(gameID)], args=[gameID, deck, startingPlayer])

drawScript = loadScript("draw.lua", r)
def draw(gameID, playerID, pile):
    return drawScript(keys=[gameKey(gameID)], args=[gameID, playerID, pile]).decode("utf-8")

discardScript = loadScript("discard.lua", r)
def discard(gameID, playerID, card):
    return discardScript(keys=[gameKey(gameID)], args=[gameID, playerID, card])

knockScript = loadScript("knock.lua", r)
def knock(gameID, playerID, melds, deadwood, discard):
    for meld in melds:
        if not isMeld(meld):
            raise ValueError("Invalid meld")
    
    if sum(card.pointValue(c) for c in deadwood) > 10:
        raise ValueError("Deadwood value > 10")

    return knockScript(
        keys=[gameKey(gameID)],
        args=[
            gameID,                 # ARGV[1]
            playerID,               # ARGV[2]
            json.dumps(melds),      # ARGV[3]
            json.dumps(deadwood),   # ARGV[4]
            discard                 # ARGV[5]
        ])

layScript = loadScript("lay.lua", r)
def lay(gameID, playerID, melds, layoffs):
    for meld in melds:
        if not isMeld(meld):
            raise ValueError("Invalid meld")
    for (m, lo) in layoffs:
        if not isMeld(m + lo):
            raise ValueError("Invalid layoff")
    return layScript(keys = [gameKey(gameID)], args = [
        gameID,
        playerID,
        json.dumps(melds),
        json.dumps(layoffs)
    ])

viewsScript = loadScript("views.lua", r)
def views(gameID):
    return json.loads(viewsScript(keys = [gameKey(gameID)]))

def randomDiscard():
    import time
    import random
    start = time.perf_counter()
    g, pl = newGame()
    joinGame(g, pl[0], "Alice")
    joinGame(g, pl[1], "Bob")
    startGame(g, pl[0])
    data = loadGameState(g)
    while not data["finished"]:
        pl = data["turn"]
        pile = random.choice(("stock", "discards"))
        dr = draw(g, pl, pile)
        dc = random.choice(data["cards"]["hands"][pl])
        discard(g, pl, dc)
        data = loadGameState(g)
    print((time.perf_counter() - start) * 1000, "ms")

def testKnock():
    g, pl = newGame()
    joinGame(g, pl[0], "Alice"); joinGame(g, pl[1], "Bob")
    startGame(g, pl[0])
    draw(g, pl[1], "stock")
    data = loadGameState(g)

    melds = [["Ah", "2h", "3h"], ["5s", "5c", "5d"], ["Jd", "Qd", "Kd"]]
    deadwood = ["Ad"]
    discard = "2d"

    melds2 = [["7c","7d","7s"]]
    layoffs = [[["Ah", "2h", "3h"], ["4h"]], [["5s", "5c", "5d"], ["5h"]], [["Jd", "Qd", "Kd"], ["9d", "Td"]]]
    deadwood2 = ["4d", "Js", "Qh"]

    data["cards"]["hands"][str(pl[0])] = [c for meld in melds for c in meld] + deadwood + [discard]
    data["cards"]["hands"][str(pl[1])] = [c for meld in melds2 for c in meld] + [c for (m,lo) in layoffs for c in lo] + deadwood2
    r.set(gameKey(g), json.dumps(data))
    
    knock(g, pl[0], melds, deadwood, discard)
    lay(g, pl[1], melds2, layoffs)

def benchmark(n):
    import time
    from collections import defaultdict
    times = defaultdict(list)
    for i in range(n):
        t = time.perf_counter()
        g, pl = newGame()
        el = time.perf_counter() - t
        times["newGame"].append(el)

        t = time.perf_counter()
        views(g)
        el = time.perf_counter() - t
        times["views"].append(el)

        t = time.perf_counter()
        joinGame(g, pl[0], "A"); joinGame(g, pl[1], "B")
        el = time.perf_counter() - t
        times["joinGame"].append(el / 2)

        t = time.perf_counter()
        views(g)
        el = time.perf_counter() - t
        times["views"].append(el)

        t = time.perf_counter()
        startGame(g, pl[0])
        el = time.perf_counter() - t
        times["startGame"].append(el)

        t = time.perf_counter()
        views(g)
        el = time.perf_counter() - t
        times["views"].append(el)

        data = loadGameState(g)

        melds = [["Ah", "2h", "3h"], ["5s", "5c", "5d"], ["Jd", "Qd", "Kd"]]
        deadwood = ["Ad"]

        melds2 = [["7c","7d","7s"]]
        layoffs = [[["Ah", "2h", "3h"], ["4h"]], [["5s", "5c", "5d"], ["5h"]], [["Jd", "Qd", "Kd"], ["9d", "Td"]]]
        deadwood2 = ["4d", "Js", "Qh"]

        stock = ["8c", "8d", "8h", "8s","6c", "6h", "6s", "6d"]

        data["cards"]["hands"][str(pl[0])] = [c for meld in melds for c in meld] + deadwood
        data["cards"]["hands"][str(pl[1])] = [c for meld in melds2 for c in meld] + [c for (m,lo) in layoffs for c in lo] + deadwood2
        data["cards"]["stock"] = stock
        r.set(gameKey(g), json.dumps(data))
        
        t = time.perf_counter()
        dr = draw(g, pl[0], "stock")
        el = time.perf_counter() - t
        times["draw"].append(el)

        t = time.perf_counter()
        views(g)
        el = time.perf_counter() - t
        times["views"].append(el)

        t = time.perf_counter()
        discard(g, pl[0], dr)
        el = time.perf_counter() - t
        times["discard"].append(el)

        t = time.perf_counter()
        views(g)
        el = time.perf_counter() - t
        times["views"].append(el)

        t = time.perf_counter()
        dr = draw(g, pl[1], "discards")
        el = time.perf_counter() - t
        times["draw"].append(el)

        t = time.perf_counter()
        views(g)
        el = time.perf_counter() - t
        times["views"].append(el)

        t = time.perf_counter()
        discard(g, pl[1], dr)
        el = time.perf_counter() - t
        times["discard"].append(el)

        t = time.perf_counter()
        views(g)
        el = time.perf_counter() - t
        times["views"].append(el)

        t = time.perf_counter()
        dr = draw(g, pl[0], "stock")
        el = time.perf_counter() - t
        times["draw"].append(el)

        t = time.perf_counter()
        views(g)
        el = time.perf_counter() - t
        times["views"].append(el)

        t = time.perf_counter()
        knock(g, pl[0], melds, deadwood, dr)
        el = time.perf_counter() - t
        times["knock"].append(el)

        t = time.perf_counter()
        views(g)
        el = time.perf_counter() - t
        times["views"].append(el)

        t = time.perf_counter()
        lay(g, pl[1], melds2, layoffs)
        el = time.perf_counter() - t
        times["lay"].append(el)

        t = time.perf_counter()
        views(g)
        el = time.perf_counter() - t
        times["views"].append(el)

    return times
    
if __name__ == "__main__":
    import statistics
    times = benchmark(1000)
    print("OP\t\tMEAN\t\tMEDIAN\t\tSTDEV")
    for op, ts in times.items():
        mean = statistics.mean(ts) * 1000
        median = statistics.median(ts) * 1000
        stdev = statistics.stdev(ts) * 1000
        print(f"{op}\t\t{mean:.3}\t\t{median:.3}\t\t{stdev:.3}")