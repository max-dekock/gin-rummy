--[[
    KEYS[1]: game:<gameID>

    ARGV[1] -> gameID
    ARGV[2] -> "".join(deck)
    ARGV[3] -> startingPlayer
--]]
if type(ARGV[2]) ~= "string" or ARGV[2]:len() ~= 104 then
    return redis.error_reply("Invalid deck argument")
end
if redis.call('exists', KEYS[1]) == 0 then
    return redis.error_reply("Error: invalid gameID")
end
local data = cjson.decode( redis.call('get', KEYS[1]) )
if data.started then
    return redis.error_reply("Cannot start game: game already started")
end
local players = data.players
local playerList = {}
for player, _ in pairs(players) do
    table.insert(playerList, player)
end

for player, status in pairs(players) do
    if not status.ready then
        return redis.error_reply("Cannot start game: player "..player.." not ready")
    end
    status.firstTurnDraw = true
end

local cards = {
    stock = {},
    discards = {},
    hands = {
        [playerList[1]] = {},
        [playerList[2]] = {}
    }
}
for i=1,103,2 do
    table.insert(cards.stock, ARGV[2]:sub(i,i+1))
end
for i=1,10 do
    table.insert(cards.hands[playerList[1]], table.remove(cards.stock))
    table.insert(cards.hands[playerList[2]], table.remove(cards.stock))
end
table.insert(cards.discards, table.remove(cards.stock))
data.cards = cards
data.turn = ARGV[3]
data.phase = "draw"
data.started = true
data.finished = false
redis.call('set', KEYS[1], cjson.encode(data), 'EX', 86400)
return redis.status_reply("OK")