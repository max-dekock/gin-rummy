<template>
  <div>
    <Melds :hand="selected"></Melds>
    <hr>
    <button @click="resetSelection">Reset hand</button>
    <Hand :cards="deck" select-mode="multi" v-model="selected"></Hand>
  </div>
</template>

<script>
import { DECK, isSet, isRun, isMeld, } from '../rummy_utils.js'
import Melds from '../components/Melds.vue'
import Hand from '../components/Hand.vue'

export default {
  data () {
    return {
      deck: DECK,
      selected: [],
    };
  },
  computed: {
    isSet() {
      return isSet(this.selected);
    },
    isRun() {
      return isRun(this.selected);
    },
    isMeld() {
      return isMeld(this.selected);
    },
  },
  methods: {
    resetSelection() {
      this.selected = [];
    }
  },
  components: {
    Melds,
    Hand,
  }
}
</script>
