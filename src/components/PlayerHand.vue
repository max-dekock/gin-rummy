<template>
  <card-sequence
    class="player-hand"
    :cards="hand"
    :options="sequenceOptions"
    @card-clicked="click"
  ></card-sequence>
</template>

<script>
import CardSequence from './CardSequence.vue'
import { mapState, mapGetters } from 'vuex'

export default {
  name: 'player-hand',
  components: {
    CardSequence
  },
  computed: {
    ...mapState({
      hand: state => state.gameData.hand,
    }),
    ...mapGetters(['uiMode', 'deadwood', 'meldSelected']),
    selected: {
      get() {
        return this.$store.state.ui.selectedCards;
      },
      set(value) {
        this.$store.commit('updateUI', {selectedCards: value});
      }
    },
    disabled() {
      let dis = new Set();
      for (let card of this.hand) {
        if (!this.deadwood.has(card)) {
          dis.add(card);
        }
      }
      return dis;
    },
    selectMode() {
      switch(this.uiMode) {
        case 'discard':
          return 'single';
        case 'knock':
        case 'lay':
          return 'multi';
        case 'draw':
        case 'wait':
        default:
          return 'off';
      }
    },
    selectColor() {
      return '#00bfff';
    },
    sequenceOptions() {
      return {
        selected: new Set(this.selected),
        selectedColor: this.selectColor,
        disabled: this.disabled,
        faceDown: false
      }
    }
  },
  methods: {
    click(card) {
      if (this.selectMode == "off") {
        this.selected = [];
        return;
      }
      if (this.disabled.has(card)) {
        return;
      }
      let newsel = this.selected;
      let i = newsel.indexOf(card);
      if (i > -1) {
        newsel.splice(i, 1);
      } else {
        switch(this.selectMode) {
          case "single":
            newsel = [card];
            break;
          case "multi":
            newsel.push(card);
            break;
        }
      }
      this.selected = newsel;
    },
  }
}
</script>