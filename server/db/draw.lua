--[[
    KEYS[1] -> game:<gameID>

    ARGV[1] -> gameID
    ARGV[2] -> playerID
    ARGV[3] -> pile
]]
local pile = ARGV[3]
if pile ~= "stock" and pile ~= "discards" and pile ~= "refuse" then
    return redis.error_reply("Error: invalid pile")
end
if redis.call('exists', KEYS[1]) == 0 then
    return redis.error_reply("Error: invalid gameID")
end
local data = cjson.decode( redis.call('get', KEYS[1]) )
if not data.players[ARGV[2]] then
    return redis.error_reply("Error: invalid playerID")
end
if not data.started then
    return redis.error_reply("Error: game not started")
end
if data.finished then
    return redis.error_reply("Error: game already finished")
end
if data.turn ~= ARGV[2] then
    return redis.error_reply("Cannot draw: not your turn")
end
if data.phase ~= "draw" then
    return redis.error_reply("Cannot draw: not draw phase")
end
if data.players[ARGV[2]].firstTurnDraw then
    if pile == "stock" then
        return redis.error_reply("Cannot draw: can't draw from stock pile on first turn")
    elseif pile == "refuse" then
        data.players[ARGV[2]].firstTurnDraw = nil
        data.turn = data.players[ARGV[2]].opponent
        redis.call('set', KEYS[1], cjson.encode(data))
        return redis.status_reply("OK")
    elseif pile == "discards" then
        for player, status in pairs(data.players) do
            status.firstTurnDraw = nil
        end
    end
end
local draw = table.remove(data.cards[pile])
table.insert(data.cards.hands[ARGV[2]], draw)
data.phase = "discard"
redis.call('set', KEYS[1], cjson.encode(data), 'EX', 86400)
return draw