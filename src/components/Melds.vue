<template>
  <div>
    <h3>Melds:</h3>
    <div class="meld" :key="i" v-for="i in melds.keys()">
      <Hand :cards="melds[i]"></Hand>
      <button @click="removeMeld(i)">Remove</button>
    </div>
    <hr>
    <Hand :cards="hand" :disabled="melded" class="hand"
      :select-color="meldOk ? 'var(--select-color-meld)' : 'var(--select-color-nomeld)'"
      select-mode="multi" v-model="selected"></Hand>
    <button @click="addMeld" :disabled="!meldOk">Add meld</button>
  </div>
</template>

<script>
import Hand from './Hand.vue'
import { isMeld } from '../rummy_utils.js'

export default {
  components: {
    Hand,
  },
  props: {
    hand: Array,
  },
  data() {
    return {
      melds: [],
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
  },
  methods: {
    addMeld() {
      console.log(`adding meld ${this.selected}`);
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
  },
};
</script>

<style>
.hand {
  --select-color-meld: lightgreen;
  --select-color-nomeld: red;
}
</style>
