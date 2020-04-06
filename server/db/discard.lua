--[[
    KEYS[1] -> game:<gameID>

    ARGV[1] -> gameID
    ARGV[2] -> playerID
    ARGV[3] -> card
--]]
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
    return redis.error_reply("Cannot discard: not your turn")
end
if data.phase ~= "discard" then
    return redis.error_reply("Cannot discard: not discard phase")
end
local cardIndex = nil
for i,c in ipairs(data.cards.hands[ARGV[2]]) do
    if c == ARGV[3] then
        cardIndex = i
        break
    end
end
if cardIndex == nil then
    return redis.error_reply("Cannot discard: card "..ARGV[3].." not in hand")
end
table.remove(data.cards.hands[ARGV[2]], cardIndex)
table.insert(data.cards.discards, ARGV[3])
if #data.cards.stock <= 2 then
    data.finished = true
    data.result = {cancelled=true}
    data.turn = nil
    data.phase = nil
else
    data.turn = data.players[ARGV[2]].opponent
    data.phase = "draw"
end
redis.call('set', KEYS[1], cjson.encode(data), 'EX', 86400)
return redis.status_reply("OK")