<template>
  <div>
    <div>
    <h3>Melds:</h3>
      <div style="display:flex; flex-wrap:nowrap;" :key="i" v-for="i in melds.keys()">
        <Hand class="meld" :cards="melds[i]"></Hand>
        <button @click="removeMeld(i)">Remove</button>
      </div>
    </div>
    <div style="display:flex; flex-wrap:nowrap;">
      <h3>Discard:</h3>
      <Card :card="discard"></Card>
      <button @click="removeDiscard" v-if="this.discard">Remove</button>
    </div>
    <hr>
    <div>
      <Hand :cards="hand" :disabled="melded.concat(discard)" class="hand"
        :select-color="meldOk ? 'var(--select-color-meld)' : 'var(--select-color-nomeld)'"
        select-mode="multi" v-model="selected"></Hand>
      <button @click="addMeld" :disabled="!meldOk">Add meld</button>
      <button @click="addDiscard" :disabled="this.discard || selected.length != 1">Discard</button>
    </div>
    <button @click="knock" :disabled="!knockOk">Knock!</button>
  </div>
</template>

<script>
import Hand from './Hand.vue'
import Card from './Card.vue'
import { isMeld, deadwoodPoints } from '../rummy_utils.js'

export default {
  components: {
    Hand,
    Card,
  },
  props: {
    hand: Array,
    maxDeadwood: {
      type: Number,
      default: 10,
    },
  },
  data() {
    return {
      melds: [],
      discard: '',
      selected: [],
    };
  },
  computed: {
    melded() {
      let m = [];
      for (let meld of this.melds) {
        for (let card of meld) {
          m.push(card);
        }
      }
      return m;
    },
    meldOk() {
      return isMeld(this.selected);
    },
    deadwood() {
      let dw = new Set(this.hand);
      dw.delete(this.discard);
      for (let meld of this.melds) {
        for (let card of meld) {
          dw.delete(card);
        }
      }
      return Array.from(dw);
    },
    dwPoints() {
      return deadwoodPoints(this.deadwood);
    },
    knockOk() {
      return (this.dwPoints <= this.maxDeadwood);
    },
  },
  methods: {
    addMeld() {
      if (!this.meldOk) {
        console.warn(`Tried to add invalid meld: ${this.selected}`);
        return;
      }
      this.melds.push(Array.from(this.selected));
      this.selected = [];
    },
    removeMeld(i) {
      this.melds.splice(i, 1);
    },
    addDiscard() {
      if (this.discard) {
        console.warn("Tried to add discard when one is already present");
        return;
      }
      if (this.selected.length != 1) {
        console.warn("Tried to add discard when selection length not 1");
        return;
      }
      this.discard = this.selected[0];
      this.selected = [];
    },
    removeDiscard() {
      this.discard = '';
    },
    knock() {
      if (!this.knockOk) {
        console.warn("Tried to knock invalidly");
        return;
      }
      let kn = {
        melds: this.melds,
        discard: this.discard,
        deadwood: this.deadwood,
        dwPoints: this.dwPoints,
      };
      this.$emit('knock', kn);
    },
  },
};
</script>

<style>
.hand {
  --select-color-meld: lightgreen;
  --select-color-nomeld: yellow;
}
</style>
