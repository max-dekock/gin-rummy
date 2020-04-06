<template>
  <div>
    <div class="gameWrapper">
      <div class="gameHeader">
        <h3 class="name">{{ currentPlayer }}'s turn</h3>
      </div>
      <div class="gameOpponentArea">
        <h4 v-if="opponentMessage">{{ opponentMessage }}</h4>
      </div>
      <div v-if="error" class="error gameInfoArea">{{ error }}</div>
      <KnockInput v-if="uiMode == 'knock'" class="gameKnockArea"></KnockInput>
      <div v-if="uiMode == 'draw' || uiMode == 'discard'" class="gameStockPile">
        <Card faceDown class="pileCard"></Card>
        <p>Stock</p>
      </div>
      <div v-if="topDiscard && (uiMode == 'draw' || uiMode == 'discard')" class="gameDiscardsPile">
        <Card :card="topDiscard" class="pileCard"></Card>
        <p>Discards</p>
      </div>
      <div v-if="uiMode == 'draw' || uiMode == 'discard'" class="gameControlArea">
        <div v-if="turn && phase == 'draw'">
          <button
            v-if="!firstTurnDraw"
            name="draw-stock"
            id="draw-stock"
            @click="draw('stock')"
          >Draw Stock</button>
          <button
            name="draw-discards"
            id="draw-discards"
            @click="draw('discards')"
          >Draw Discard</button>
          <button
            v-if="firstTurnDraw"
            name="draw-refuse"
            id="draw-refuse"
            @click="draw('refuse')"
          >Pass</button>
        </div>
        <div v-else-if="turn && phase == 'discard'">
          <button
            name="discard"
            id="discard"
            @click="discard(selectedCards[0])"
            :disabled="selectedCards.length != 1"
          >Discard</button>
          <button
            name="knockInput"
            id="knockInput"
            @click="updateUI({knockMode: true})"
          >Knock</button>
        </div>
        <div v-else>
          <p>{{ opponent }} is {{ phase }}ing...</p>
        </div>
      </div>
      <div class="gameHandArea">
        <player-hand></player-hand>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
import Card from '../components/Card.vue'
import PlayerHand from '../components/PlayerHand.vue'
import KnockInput from '../components/KnockInput.vue'

export default {
  components: {
    Card,
    PlayerHand,
    KnockInput
  },
  computed: {
    ...mapState({
      started: state => state.gameData.started,
      turn: state => state.gameData.turn,
      phase: state => state.gameData.phase,
      hand: state => state.gameData.hand,
      topDiscard: state => state.gameData.topDiscard,
      opponent: state => state.gameData.opponent,
      username: state => state.gameData.nickname,
      firstTurnDraw: state => state.gameData.firstTurnDraw,
      error: state => state.error,
      uiMode: (state, getters) => getters.uiMode,
    }),
    currentPlayer() {
      return this.turn ? this.username : this.opponent;
    },
    selectedCards: {
      get() {
        return this.$store.state.ui.selectedCards;
      },
      set(value) {
        this.$store.commit('updateUI', {selectedCards: value});
      }
    },
    handSelectMode() {
      if (this.turn && this.phase == 'discard') {
        if (this.uiMode == 'knock') {
          return 'multi';
        } else {
          return 'single';
        }
      } else if (this.turn && this.phase == 'lay')  {
        return 'multi'
      } else {
        return 'off';
      }
    },
    opponentMessage() {
      return '';
    }
  },
  methods: {
    ...mapMutations(['updateUI']),
    draw(pile) {
      this.$store.dispatch('draw', pile);
    },
    discard(card) {
      this.$store.dispatch('discard', card);
      this.selectedCard = [];
    }
  }
}
</script>

<style>
.pileCard {
  margin: auto;
}
.gameWrapper {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-auto-rows: minmax(50px, auto);
  grid-gap: 10px;
}
.gameHeader {
  grid-column: 1 / 6;
  grid-row: 1;
}
.gameOpponentArea {
  grid-column: 1 / 6;
  grid-row: 2;
}
.gameInfoArea {
  grid-column: 2 / 5;
  grid-row: 3;
}
.gameStockPile {
  grid-column: 2;
  grid-row: 4;
}
.gameDiscardsPile {
  grid-column: 4;
  grid-row: 4;
}
.gameControlArea {
  grid-column: 2 / 5;
  grid-row: 5;
}
.gameKnockArea {
  grid-column: 1 / 6;
  grid-row: 4 / 6;
}
.gameHandArea {
  grid-column: 1 / 6;
  grid-row: 6;
}
.gameFooter {
  grid-column: 1 / 6;
  grid-row: 7;
}

</style>
