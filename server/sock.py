from flask import request
from flask_socketio import SocketIO, emit, join_room
from .db import op
import traceback

def create_socketio():
    socketio = SocketIO(cors_allowed_origins="*")

    def updatePlayers(gameID):
        game = op.loadGameState(gameID)
        for playerID in game["players"]:
            data = game.copy()
            del data["cards"]
            del data["players"]
            data["turn"] = game["turn"] == playerID
            data["player_id"] = playerID
            data["game_id"] = gameID
            data["username"] = game["usernames"][playerID]
            data["opponent"] = game["usernames"][game["opponents"][playerID]]
            data["hand"] = game["cards"]["hands"][playerID]
            data["topdiscard"] = game["cards"]["discards"][-1]

            socketio.emit("update", data, room=playerID)

    @socketio.on("create")
    def onCreate(data):
        if "playerID" in data:
            playerID = data["player_id"]
            username = op.loadPlayerState(playerID)["username"]
        else:
            playerID = op.createPlayer(data["username"])
            username = data["username"]
        gameID = op.createGame()
        op.joinGame(gameID, playerID)
        
        join_room(gameID)
        join_room(playerID)
        emit("join", {"player_id": playerID, "game_id": gameID, "username": username})

    @socketio.on("join")
    def onJoin(data):
        if "playerID" in data:
            playerID = data["player_id"]
            username = op.loadPlayerState(playerID)["username"]
        else:
            playerID = op.createPlayer(data["username"])
            username = data["username"]
        gameID = data["game_id"]
        op.joinGame(gameID, playerID)

        join_room(gameID)
        join_room(playerID)
        emit("join", {"player_id": playerID, "game_id": gameID, "username": username})

        gameData = op.loadGameState(gameID)
        if len(gameData["players"]) == 2:
            op.startGame(gameID, playerID)
            updatePlayers(gameID)

    @socketio.on("draw")
    def onDraw(data):
        playerID = data["player_id"]
        gameID = data["game_id"]
        op.draw(gameID, playerID, data["pile"])
        updatePlayers(gameID)

    @socketio.on("discard")
    def onDiscard(data):
        playerID = data["player_id"]
        gameID = data["game_id"]
        op.discard(gameID, playerID, data["card"])
        updatePlayers(gameID)

    @socketio.on("knock")
    def onKnock(data):
        playerID = data["player_id"]
        gameID = data["game_id"]
        melds = data["melds"]
        deadwood = data["deadwood"]
        discard = data["discard"]
        op.knock(gameID, playerID, melds, deadwood, discard)
        updatePlayers(gameID)

    @socketio.on("lay")
    def onLay(data):
        playerID = data["player_id"]
        gameID = data["game_id"]
        melds = data["melds"]
        layoffs = data["layoffs"]
        op.lay(gameID, playerID, melds, layoffs)
        updatePlayers(gameID)

    @socketio.on_error()
    def onError(e):
        traceback.print_exc()
        print(request.event["message"])
        print(request.event["args"])
        emit('error', {"error": str(e)})
    
    return socketio