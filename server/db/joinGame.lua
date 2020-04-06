--[[
    KEYS[1] -> game:<gameID>

    ARGV[1] -> gameID
    ARGV[2] -> playerID
    ARGV[3] -> nickname
--]]
if redis.call('exists', KEYS[1]) == 0 then
    return redis.error_reply("Error: invalid gameID")
end
local gameData = cjson.decode( redis.call('get', KEYS[1]) )
local validPlayer = false
for player, status in pairs(gameData.players) do
    if player == ARGV[2] then
        if status.ready then
            return redis.error_reply(string.format('Error: player %s already joined', player))
        else
            status.ready = true
            status.nickname = ARGV[3]
            validPlayer = true
            break
        end
    end
end

if not validPlayer then
    return redis.error_reply('Error: invalid playerID')
end

redis.call('set', KEYS[1], cjson.encode(gameData), 'EX', 86400)
return cjson.encode(gameData.players)