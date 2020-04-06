from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, send, emit, join_room

import random
import traceback
import os
import base64

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = "dev"

from .rummy.model import Rummy

games = {}
players = {}

def create_game():
    while True:
        game_id = str(base64.urlsafe_b64encode(os.urandom(6)), 'utf-8')
        if game_id not in games:
            break
    games[game_id] = { "players": [], "model": None, "started": False }
    return game_id

def create_player(username):
    while True:
        player_id = str(base64.urlsafe_b64encode(os.urandom(6)), 'utf-8')
        if player_id not in players:
            break
    players[player_id] = {"username": username}
    return player_id

def join_game(player_id, game_id):
    if game_id not in games:
        raise Exception("Game not found")
    game = games[game_id]
    if player_id in game["players"]:
        # already in game
        return
    if len(game["players"]) >= 2:
        raise Exception("Game already full")
    game["players"].append(player_id)
    players[player_id]["game_id"] = game_id

    if len(game["players"]) == 2:
        start_game(game_id)

def start_game(game_id):
    print(f"Starting game {game_id}...")
    if game_id not in games:
        raise Exception('Game not found')
    model = Rummy(*games[game_id]['players'])
    model.deal()
    games[game_id]["started"] = True
    games[game_id]["model"] = model
    print(games[game_id])
    print(model.players)
    print(model.currentplayer)
    update_all(game_id)

def update_all(game_id):
    print(f"Updating players in game {game_id}...")
    for player_id in games[game_id]["players"]:
        update(player_id, game_id)

def update(player_id, game_id):
    print(f"Updating player {player_id}...")
    data = {"player_id":player_id, "game_id":game_id}
    data["username"] = players[player_id]["username"]
    started = games[game_id]["started"]
    data['started'] = started
    if started:
        model = games[game_id]['model']
        data['opponent'] = players[model.opponent(player_id)]["username"]
        data['hand'] = model.hands[player_id]
        data['topdiscard'] = model.top_discard()
        data['turn'] = model.currentplayer == player_id
        data['phase'] = model.phase
    socketio.emit('update', data, room=player_id)

@socketio.on('create')
def on_create(data):
    print("creating game...")
    print(data)
    username = data["username"]
    game_id = create_game()
    player_id = create_player(username)
    join_room(player_id)
    emit('join', {"player_id": player_id, "game_id": game_id, "username": username})
    join_game(player_id, game_id)


@socketio.on('join')
def on_join(data):
    username = data["username"]
    game_id = data["game_id"]
    player_id = create_player(username)
    join_room(player_id)
    emit('join', {"player_id": player_id, "game_id": game_id, "username": username})
    join_game(player_id, game_id)

@socketio.on('draw')
def on_draw(data):
    print(data)
    player_id = data["player_id"]
    game_id = data["game_id"]
    model = games[game_id]["model"]
    model.draw(player_id, data["pile"])
    update_all(game_id)

@socketio.on('discard')
def on_discard(data):
    print(data)
    player_id = data["player_id"]
    game_id = data["game_id"]
    model = games[game_id]["model"]
    model.discard(player_id, data["card"])
    update_all(game_id)

@socketio.on_error()
def error_handler(e):
    traceback.print_exc()
    print(request.event["message"])
    print(request.event["args"])
    emit('error', {"error": str(e)})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port="5000", debug=True)
