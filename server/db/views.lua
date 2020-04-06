--[[
    KEYS[0]: game:<gameID>
--]]
if redis.call('exists', KEYS[1]) == 0 then
    return redis.error_reply("Error: game not found")
end
local data = cjson.decode( redis.call('get', KEYS[1]) )
local players = data.players
local started = data.started
local views = {}
for player, status in pairs(players) do
    local view = {}
    local subj = {[player]='you', [status.opponent]='opponent'}
    view.started = started
    view.nickname = status.nickname
    if started then
        view.firstTurnDraw = status.firstTurnDraw
        local opponent = status.opponent
        view.opponent = players[opponent].nickname
        local finished = data.finished
        view.finished = finished
        view.topDiscard = data.cards.discards[#data.cards.discards]
        if data.result then
            view.result = {}
            for key, value in pairs(data.result) do
                if type(value) == 'table' then
                    view.result[key] = {}
                    for player, entry in pairs(value) do
                        view.result[key][subj[player]] = entry
                    end
                elseif subj[value] then
                    view.result[key] = subj[value]
                else
                    view.result[key] = value
                end
            end
        end
        if not finished then
            view.hand = data.cards.hands[player]
            view.turn = data.turn == player
            view.phase = data.phase
        end
    end
    views[player] = view
end
return cjson.encode(views)