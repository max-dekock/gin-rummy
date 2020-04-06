from .rummy import card
from .db import op
from flask import request
from flask_socketio import SocketIO, Namespace, emit, join_room
import traceback

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on('newGame')
def onNewGame(payload):
    nickname = payload['nickname']
    gameID, plids = op.newGame()
    playerID = plids[0]
    joinCode = op.joinCode(gameID, plids[1])
    op.joinGame(gameID, playerID, nickname)
    join_room(f'game:{gameID}')
    join_room(f'player:{playerID}')
    emit('newGame', {'message': 'OK', 'gameID': gameID, 'playerID': playerID, 'nickname':nickname, 'joinCode': joinCode})
    updateGame(gameID)

@socketio.on('joinGame')
def onJoinGame(payload):
    nickname = payload['nickname']
    if 'joinCode' in payload:
        decode = op.joinDecode(payload['joinCode'])
        gameID = decode['gameID']
        playerID = decode['playerID']
    else:
        gameID = payload['gameID']
        playerID = payload['playerID']
    players = op.joinGame(gameID, playerID, nickname)
    join_room(f'game:{gameID}')
    join_room(f'player:{playerID}')
    emit('joinGame', {'message': 'OK', 'gameID': gameID, 'playerID': playerID, 'nickname': nickname})
    if all(status['ready'] for status in players.values()):
        op.startGame(gameID, playerID)
    updateGame(gameID)

@socketio.on('draw')
def onDraw(payload):
    gameID = payload['gameID']
    playerID = payload['playerID']
    pile = payload['pile']
    card = op.draw(gameID, playerID, pile)
    if pile != 'refuse':
        emit('draw', {'message': 'OK', 'card': card})
    updateGame(gameID)

@socketio.on('discard')
def onDiscard(payload):
    gameID = payload['gameID']
    playerID = payload['playerID']
    card = payload['card']
    op.discard(gameID, playerID, card)
    emit('discard', {'message': 'OK', 'card': card})
    updateGame(gameID)

@socketio.on('knock')
def onKnock(payload):
    gameID = payload['gameID']
    playerID = payload['playerID']
    melds = payload['melds']
    if 'deadwood' in payload:
        deadwood = payload['deadwood']
    else:
        deadwood = []
    discard = payload['discard']
    op.knock(gameID, playerID, melds, deadwood, discard)
    deadwoodPoints = sum(card.pointValue(c) for c in deadwood)
    emit('knock', {'message': 'OK', 'deadwoodPoints': deadwoodPoints})
    updateGame(gameID)

@socketio.on('lay')
def onLay(payload):
    gameID = payload['gameID']
    playerID = payload['playerID']
    melds = payload['melds']
    if 'layoffs' in payload:
        layoffs = payload['layoffs']
    else:
        layoffs = []
    op.lay(gameID, playerID, melds, layoffs)
    emit('lay', {'message': 'OK'})
    updateGame(gameID)

@socketio.on('update')
def onUpdate(payload):
    if 'gameID' in payload:
        updateGame(payload['gameID'])

def updateGame(gameID):
    views = op.views(gameID)
    for player, view in views.items():
        if 'finished' in view and view['finished']:
            view['score'] = scoreResult(view['result'])
        socketio.emit('update', view, room=f'player:{player}')

def scoreResult(result):
    if 'cancelled' in result:
        return {'you': 0, 'opponent': 0}
    knock = result['knocker']
    if knock == 'you':
        other = 'opponent'
    elif knock == 'opponent':
        other = 'you'
    knock_dw = sum(card.pointValue(c) for c in result['deadwood'][knock])
    other_dw = sum(card.pointValue(c) for c in result['deadwood'][other])
    if knock_dw == 0:
        return {knock: other_dw + 20, other: 0}
    elif knock_dw < other_dw:
        return {knock: other_dw - knock_dw, other: 0}
    else:
        return {knock: 0, other: knock_dw - other_dw + 10}

@socketio.on_error()
def onError(e):
    traceback.print_exc()
    print(request.event["message"])
    print(request.event["args"])
    emit('error', {"error": str(e)})

if __name__ == '__main__':
    from . import create_app
    import time
    app = create_app()
    socketio.init_app(app)
    client = socketio.test_client(app)
    client.emit('newGame', {'nickname': 'Drake Bell'})
    r = client.get_received()
    r = r[0]['args'][0] 
    g = r['gameID']
    p1 = r['playerID']
    jc = r['joinCode']
    client.emit('joinGame', {'joinCode': jc, 'nickname': 'Josh Peck'})
    r = client.get_received()
    p2 = r[0]['args'][0]['playerID']
    client.emit('draw', {'gameID': g, 'playerID': p2, 'pile': 'refuse'})
    print(client.get_received())
    client.emit('draw', {'gameID': g, 'playerID': p1, 'pile': 'refuse'})
    r = client.get_received()
    print(r)
    client.emit('draw', {'gameID': g, 'playerID': p2, 'pile': 'stock'})

