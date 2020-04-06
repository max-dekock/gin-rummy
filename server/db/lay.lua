--[[
    KEYS[1]: game:<gameID>

    ARGV[1]: gameID
    ARGV[2]: playerID
    ARGV[3]: melds (json)
    ARGV[4]: deadwood (json)
    ARGV[5]: discard
--]]
if redis.call('exists', KEYS[1]) == 0 then
    return redis.error_reply("Error: game not found")
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
if data.phase ~= "lay" then
    return redis.error_reply("Cannot lay: not lay phase")
end
if data.turn ~= ARGV[2] then
    return redis.error_reply("Cannot lay: you knocked!")
end


local hand = data.cards.hands[ARGV[2]]
local melds = cjson.decode(ARGV[3])
local layoffs = cjson.decode(ARGV[4])
local opponent = data.players[ARGV[2]].opponent
local opponentMelds = data.result.melds[opponent]
if layoffs ~= nil and data.gin == true then
    return redis.error_reply("Cannot lay: opponent went gin, no layoffs permitted")
end
local rem = {}
for i,c in ipairs(hand) do
    rem[c] = true
end
for i,m in ipairs(melds) do
    for i,c in ipairs(m) do
        if not rem[c] then
            return redis.error_reply("Cannot lay: card not in hand or duplicated")
        end
        rem[c] = false
    end
end
for i,mlo in ipairs(layoffs) do
    local m = mlo[1]
    local lo = mlo[2]
    local valid = false
    for i,om in ipairs(opponentMelds) do
        local cc = {}
        for i,c in ipairs(om) do
            cc[c] = true
        end
        local invalid = false
        for i,c in ipairs(m) do
            if cc[c] then
                cc[c] = false
            else
                invalid = true
                break
            end
        end
        if not invalid then
            for k,v in pairs(cc) do
                if v then
                    invalid = true
                    break
                end
            end
            if not invalid then
                valid = true
                break
            end
        end

    end
    if not valid then
        return redis.error_reply("Cannot lay: opponent has no such meld")
    end
    for i,c in ipairs(lo) do
        if not rem[c] then
            return redis.error_reply("Cannot lay: card not in hand or duplicated")
        end
        rem[c] = false
    end
end
local deadwood = {}
for k,v in pairs(rem) do
    if v then
        table.insert(deadwood, k)
    end
end

data.result.melds[ARGV[2]] = melds
data.result.layoffs = {[ARGV[2]] = layoffs}
data.result.deadwood[ARGV[2]] = deadwood

data.finished = true
data.turn = nil
data.phase = nil

redis.call('set', KEYS[1], cjson.encode(data), 'EX', 86400)
return redis.status_reply("OK")