import pytest
import json
import redis
import random

from server.db import redis_client, op

@pytest.fixture
def invalid_game():
    gid = "totally invalid gameID"
    redis_client.delete(gid) # just making sure!
    return gid

@pytest.fixture
def started_game():
    data = op.newGame()
    for p in data[1]:
        op.joinGame(data[0], p, "test")
    op.startGame(data[0], data[1][0])
    return data

def test_newGame():
    gameID, playerIDs = op.newGame()
    assert gameID
    assert len(playerIDs) == 2
    gameData = json.loads(redis_client.get(f'game:{gameID}'))
    assert len(gameData) > 0
    for playerID in playerIDs:
        assert playerID in gameData['players']
        assert gameData['players'][playerID]['ready'] == False
        assert gameData['players'][playerID]['opponent'] in gameData['players']
    assert gameData['started'] == False

def test_joinGame(invalid_game):
    with pytest.raises(redis.ResponseError):
        op.joinGame(invalid_game, "arbitrary playerID", "arbitrary nickname")
    
    gameID, playerIDs = op.newGame()

    with pytest.raises(redis.ResponseError):
        op.joinGame(gameID, "invalid playerID", "arbitrary nickname")

    for playerID in playerIDs:
        op.joinGame(gameID, playerID, "test")
        gameData = json.loads(redis_client.get(f'game:{gameID}'))
        assert gameData['players'][playerID]['ready'] == True
        assert gameData['players'][playerID]['nickname'] == 'test'

        with pytest.raises(redis.ResponseError):
            # already joined game
            op.joinGame(gameID, playerID, "already joined")

def test_joinCode():
    jc = op.joinCode("arbitrary gameID", "arbitrary playerID")
    data = op.joinDecode(jc)
    assert data['gameID'] == "arbitrary gameID"
    assert data['playerID'] == "arbitrary playerID"

def test_startGame(invalid_game):
    with pytest.raises(redis.ResponseError):
        op.startGame(invalid_game, "arbitrary staring player")

    gameID, playerIDs = op.newGame()

    for playerID in playerIDs:
        with pytest.raises(redis.ResponseError):
            op.startGame(gameID, playerID)
        op.joinGame(gameID, playerID, "test")
    
    op.startGame(gameID, playerIDs[0])
    gameData = json.loads(redis_client.get(f'game:{gameID}'))
    assert gameData['started'] == True
    assert gameData['turn'] == playerIDs[0]
    assert gameData['phase'] == 'draw'
    for playerID in playerIDs:
        assert gameData['players'][playerID]['firstTurnDraw'] == True

def test_draw(invalid_game, started_game):
    with pytest.raises(redis.ResponseError):
        op.draw(invalid_game, "arbitrary player", "arbitrary pile")

    gid, (p1, p2) = started_game
    data1 = op.loadGameState(gid)
    topDiscard = data1['cards']['discards'][-1]
    lenDiscards = len(data1['cards']['discards'])
    hands1 = data1['cards']['hands']
    for p in (p1, p2):
        assert topDiscard not in hands1[p]
    with pytest.raises(redis.ResponseError):
        # wrong turn
        op.draw(gid, p2, "discards")
    with pytest.raises(redis.ResponseError):
        # can't draw stock on first turn
        op.draw(gid, p1, "stock")
    
    op.draw(gid, p1, "refuse")
    data2 = op.loadGameState(gid)
    assert data2['cards']['discards'][-1] == topDiscard
    for p in (p1, p2):
        assert data2['cards']['hands'][p] == hands1[p]
    assert data2['turn'] == p2
    assert data2['phase'] == 'draw'

    op.draw(gid, p2, "discards")
    data3 = op.loadGameState(gid)
    discards3 = data3['cards']['discards']
    hands3 = data3['cards']['hands']
    assert len(discards3) == lenDiscards - 1
    assert hands3 == data3['cards']['hands']
    assert len(hands3[p2]) == 11
    assert topDiscard in hands3[p2]
    assert topDiscard not in hands3[p1]
    assert data3['turn'] == p2
    assert data3['phase'] == 'discard'

    topStock = data3['cards']['stock'][-1]
    op.discard(gid, p2, topDiscard)
    op.draw(gid, p1, 'stock')
    data4 = op.loadGameState(gid)
    assert topStock in data4['cards']['hands'][p1]

def test_discard(invalid_game, started_game):
    with pytest.raises(redis.ResponseError):
        op.discard(invalid_game, "arbitrary player", "arbitrary card")
    
    gid, (p1, p2) = started_game

    with pytest.raises(redis.ResponseError):
        # incorrect phase
        op.discard(gid, p1, "arbitrary card")
    
    op.draw(gid, p1, 'discards')
    gameData = op.loadGameState(gid)
    dc = gameData['cards']['hands'][p1][0]
    op.discard(gid, p1, dc)
    gameData = op.loadGameState(gid)
    assert gameData['turn'] == p2
    assert gameData['phase'] == 'draw'
    assert len(gameData['cards']['hands'][p2]) == 10
    assert dc not in gameData['cards']['hands'][p2]
    assert gameData['cards']['discards'][-1] == dc

    while not gameData['finished']:
        p = gameData['turn']
        op.draw(gid, p, random.choice(('stock', 'discards')))
        dc = random.choice(gameData['cards']['hands'][p])
        op.discard(gid, p, dc)
        gameData = op.loadGameState(gid)
        assert len(gameData['cards']['hands'][p]) == 10
        assert dc not in gameData['cards']['hands'][p]
        assert gameData['cards']['discards'][-1] == dc
    
    assert gameData['finished']
    assert len(gameData['cards']['stock']) == 2

def test_knock(invalid_game, started_game):
    with pytest.raises(redis.ResponseError):
        op.knock(invalid_game, "", [], [], "")
    
    gid, (p1, p2) = started_game

    melds = [["Ah", "2h", "3h"], ["5s", "5c", "5d"], ["Jd", "Qd", "Kd"]]
    deadwood = ["Ad"]
    discard = "2d"

    with pytest.raises(redis.ResponseError):
        # wrong phase
        op.knock(gid, p1, melds, deadwood, discard)
    
    gameData = op.loadGameState(gid)
    gameData['phase'] = 'discard'
    redis_client.set(op.gameKey(gid), json.dumps(gameData))

    with pytest.raises(ValueError):
        # invalid meld
        op.knock(gid, p1, [["Qh", "Qd", "Qs", "7c"]], [], "")
    with pytest.raises(ValueError):
        # excessive deadwood
        op.knock(gid, p1, melds, ["10s", "Jd"], "")
    with pytest.raises(redis.ResponseError):
        # cards not in hand
        op.knock(gid, p1, melds, deadwood, discard)

    gameData = op.loadGameState(gid)
    gameData['cards']['hands'][p1] = [c for meld in melds for c in meld] + deadwood + [discard]
    redis_client.set(op.gameKey(gid), json.dumps(gameData))

    op.knock(gid, p1, melds, deadwood, discard)
    gameData = op.loadGameState(gid)
    assert gameData['cards']['discards'][-1] == discard
    assert gameData['result']['knocker'] == p1
    assert gameData['result']['melds'][p1] == melds
    assert gameData['result']['deadwood'][p1] == deadwood
    assert gameData['turn'] == p2
    assert gameData['phase'] == 'lay'

def test_lay(invalid_game, started_game):
    with pytest.raises(ValueError):
        op.lay(invalid_game, "", [], [])
    
    gid, (p1, p2) = started_game
    print(gid)

    melds = [["Ah", "2h", "3h"], ["5s", "5c", "5d"], ["Jd", "Qd", "Kd"]]
    deadwood = ["Ad"]
    discard = "2d"
    hand1 = [c for meld in melds for c in meld] + deadwood + [discard]

    melds2 = [["7c","7d","7s"]]
    layoffs = [[0, ["4h"]], [1, ["5h"]], [2, ["9d", "Td"]]]
    deadwood2 = ["4d", "Js", "Qh"]
    hand2 = [c for meld in melds2 for c in meld] + deadwood2 + [c for lo in layoffs for c in lo[1]]

    gameData = op.loadGameState(gid)
    gameData['cards']['hands'][p1] = hand1
    gameData['cards']['hands'][p2] = hand2
    gameData['phase'] = 'discard'
    redis_client.set(op.gameKey(gid), json.dumps(gameData))

    op.knock(gid, p1, melds, deadwood, discard)
    op.lay(gid, p2, melds2, layoffs)
    gameData = op.loadGameState(gid)
    assert gameData['result']['melds'][p2] == melds2
    assert set(gameData['result']['deadwood'][p2]) == set(deadwood2)
    assert gameData['result']['layoffs'][p2] == layoffs
    assert gameData['finished'] == True

def test_views():
    # TODO
    assert 0