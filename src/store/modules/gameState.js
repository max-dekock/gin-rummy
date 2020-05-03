const other = {
    you: 'opponent',
    opponent: 'you'
}

const state = {
    started: false,
    finished: false,
    nickname: '',
    opponent: '',
    turn: false,
    phase: '',
    topDiscard: '',
    hand: [],
    firstTurnDraw: false,
    knocker: '',
    melds: {},
    layoffs: {},
    deadwood: {},
    score: {},
}

const getters = {
    currentPlayer(state) {
        if (state.started && !state.finished) {
            return state.turn ? state.nickname : state.opponent;
        }
    },
    gin(state) {
        if (!state.knocker) {
            return false;
        } else {
            return (state.deadwood[state.knocker].length == 0);
        }
    },
    undercut(state) {
        if (!state.finished || !state.knocker) {
            return false;
        } else {
            return state.score[state.knocker] < state.score[other[state.knocker]];
        }
    },
    winner(state) {
        if (state.finished) {
            if (state.score.you > state.score.opponent)             {
                return 'you';
            } else if (state.score.opponent > state.score.you) {
                return 'opponent';
            }
        }
    }
}

const mutations = {
    SOCKET_UPDATE(state, payload) {
        // TODO fix server code to avoid dumb workarounds
        if (payload.result) {
            payload = {...payload.result, ...payload};
        }
        for (let key in payload) {
            if (key in state) {
                state[key] = payload[key];
            }
        }
        for (let key in state.deadwood) {
            if (Object.keys(state.deadwood[key]).length == 0) {
                state.deadwood[key] = [];
            }
        }
        if (state.finished) {
            state.turn = false;
            state.phase = 'finished';
        }
        if (!('firstTurnDraw' in payload)) {
            state.firstTurnDraw = false; 
        }
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations
}