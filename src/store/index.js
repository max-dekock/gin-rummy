import Vue from 'vue'
import Vuex from 'vuex'
import gameState from './modules/gameState.js'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    gameState,
  },
  state: {
    error: '',
    gameID: '',
    playerID: '',
    joinCode: '',
  },
  getters: {

  },
  mutations: {
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
  },
  actions: {
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
    knock({state}, {melds, discard, deadwood}) {
      this._vm.$socket.client.emit('knock', {
        gameID: state.gameID,
        playerID: state.playerID,
        melds,
        discard,
        deadwood,
      });
    },
    lay({state}, {melds, layoffs}) {
      this._vm.$socket.client.emit('lay', {
        gameID: state.gameID,
        playerID: state.playerID,
        melds,
        layoffs: layoffs.map((val, index) => [index, val]).filter(() => true),
      });
    }
  },
});
