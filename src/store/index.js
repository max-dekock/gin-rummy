import Vue from 'vue'
import Vuex from 'vuex'
import { isMeld, deadwoodPoints } from '../rummy_utils.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    error: '',
    gameID: '',
    playerID: '',
    joinCode: '',
    gameData: {},
    ui: {
      selectedCards: [],
      knockMode: false,
      melds: [],
      knockDiscard: '',
      layoffs: [],
    }
  },
  getters: {
    gameStarted(state) {
      if (state.gameData.started) {
        return true;
      } else {
        return false;
      }
    },
    gameFinished(state) {
      if (state.gameData.finished) {
        return true;
      } else {
        return false;
      }
    },
    uiMode(state) {
      if (!state.gameData.turn) {
        return 'wait'
      } else if (state.gameData.phase == 'discard') {
        return state.ui.knockMode ? 'knock' : 'discard';
      } else {
        return state.gameData.phase;
      }
    },
    deadwood({gameData, ui}, {uiMode}) {
      let dw = new Set(gameData.hand);
      if (uiMode == 'knock') {
        dw.delete(ui.knockDiscard);
        for (let meld of ui.melds) {
          for (let card of meld) {
            dw.delete(card);
          }
        }
      } else if (uiMode == 'lay') {
        for (let meld of ui.melds) {
          for (let card of meld) {
            dw.delete(card);
          }
        }
        for (let i in ui.layoffs) {
          for (let card of ui.layoffs[i]) {
            dw.delete(card);
          }
        }
      }
      return dw;
    },
    deadwoodPoints(state, {deadwood}) {
      return deadwoodPoints(deadwood);
    },
    knockValid(state, {deadwoodPoints}) {
      return (deadwoodPoints <= 10);
    },
    meldSelected({ui}, {deadwood}) {
      if (!isMeld(ui.selectedCards)) {
        return false;
      }
      for (let card of ui.selectedCards) {
        if (!deadwood.has(card)) {
          return false;
        }
      }
      return true;
    }
  },
  mutations: {
    updateUI(state, newui) {
      Object.assign(state.ui, newui);
    },
    resetUI(state) {
      state.ui = {
        selectedCards: [],
        knockMode: false,
        melds: [],
        knockDiscard: '',
        layoffs: [],
      };
    },
    SOCKET_UPDATE(state, payload) {
      state.gameData = payload;
    },
    SOCKET_ERROR(state, data) {
      console.warn(`Server error: ${data.error}`);
      state.error = data.error;
      this._vm.$socket.client.emit('update', {gameID: state.gameID, playerID: state.playerID});
    },
    SOCKET_NEWGAME(state, payload) {
      state.gameID = payload.gameID;
      state.playerID = payload.playerID;
      state.joinCode = payload.joinCode;
    },
    SOCKET_JOINGAME(state, payload) {
      state.gameID = payload.gameID;
      state.playerID = payload.playerID;
    },
    SOCKET_DISCARD(state) {
      state.ui.selectedCards = [];
    }
  },
  actions: {
    addMeld({state, getters, commit}) {
      if (getters.meldSelected) {
        let meld = Array.from(state.ui.selectedCards);
        let newMelds = Array.from(state.ui.melds);
        newMelds.push(meld);
        commit('updateUI', {melds: newMelds, selectedCards: []});
      }
    },
    removeMeld({state, commit}, meldKey) {
      let newMelds = Array.from(state.ui.melds);
      newMelds.splice(meldKey, 1);
      commit('updateUI', {melds: newMelds});
    },
    draw({state}, pile) {
      this._vm.$socket.client.emit('draw', {
        gameID: state.gameID,
        playerID: state.playerID,
        pile: pile
      });
    },
    discard({state}, card) {
      this._vm.$socket.client.emit('discard', {
        gameID: state.gameID,
        playerID: state.playerID,
        card: card
      });
    },
    knock({state, getters}) {
      this._vm.$socket.client.emit('knock', {
        gameID: state.gameID,
        playerID: state.playerID,
        melds: state.ui.melds,
        discard: state.ui.knockDiscard,
        deadwood: Array.from(getters.deadwood),
      });
    },
    lay({state}) {
      let layoffs = [];
      for (let i in state.ui.layoffs) {
        layoffs.push([state.gameData.result.melds.opponent[i], state.ui.layoffs[i]]);
      }
      this._vm.$socket.client.emit('lay', {
        gameID: state.gameID,
        playerID: state.playerID,
        melds: state.ui.melds,
        layoffs: layoffs,
      });
    }
  },
});
