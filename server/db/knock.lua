--[[
    KEYS[1]: game:<gameID>

    ARGV[1]: gameID
    ARGV[2]: playerID
    ARGV[3]: melds (json)
    ARGV[4]: deadwood (json)
    ARGV[5]: discard
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
    return redis.error_reply("Cannot knock: not your turn")
end
if data.phase ~= "discard" then
    return redis.error_reply("Cannot knock: not discard phase")
end

local hand = data.cards.hands[ARGV[2]]
local melds = cjson.decode(ARGV[3])
local deadwood = cjson.decode(ARGV[4])
local discard = ARGV[5]
local rem = {}
local discardIndex = nil
for i,c in ipairs(hand) do
    rem[c] = true
    if c == discard then
        discardIndex = i
    end
end
if not rem[discard] then
    return redis.error_reply("Cannot knock: discard "..discard.." not in hand or duplicate")
end
rem[discard] = false
for i,c in ipairs(deadwood) do
    if not rem[c] then
        return redis.error_reply("Cannot knock: deadwood card "..c.." not in hand or duplicate")
    end
    rem[c] = false
end
for i,m in ipairs(melds) do
    for i,c in ipairs(m) do
        if not rem[c] then
            return redis.error_reply("Cannot knock: meld card "..c.." not in hand or duplicate")
        end
        rem[c] = false
    end
end
for k,v in pairs(rem) do
    if v then
        return redis.error_reply("Cannot knock: card "..k.." in hand, not in knock")
    end
end

data.result = {}
data.result.knocker = ARGV[2]
if #deadwood == 0 then
    data.result.gin = true
else
    data.result.gin = false
end
data.result.melds = { [ARGV[2]] = melds }
data.result.deadwood = { [ARGV[2]] = deadwood }
if discard then
    table.remove(data.cards.hands[ARGV[2]], discardIndex)
    table.insert(data.cards.discards, discard)
end

data.turn = data.players[ARGV[2]].opponent
data.phase = 'lay'

redis.call('set', KEYS[1], cjson.encode(data), 'EX', 86400)
return redis.status_reply("OK")