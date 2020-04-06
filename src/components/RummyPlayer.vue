<template>
  <div>
    <h3 class="name">{{ username }}</h3>
    <Hand :cards="hand" v-model="discardcard"></Hand>
    <div>Top of discard pile: <span class="card">{{ topdiscard }}</span></div>
    <div v-if="turn && phase == 'draw'">
      <button name="draw-stock" id="draw-stock" @click="draw('stock')">Draw Stock</button>
      <button name="draw-discard" id="draw-discard" @click="draw('discards')">Draw Discard</button>
    </div>
    <div v-else-if="turn && phase == 'discard'">
      <button name="discard" id="discard" @click="discard(discardcard)" :disabled="!discardcard">Discard</button>
    </div>
    <div v-else>
      <p>{{ opponent }} is {{ phase }}ing...</p>
    </div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Hand from './Hand.vue'

export default {
  components: {
    Hand
  },
  data() {
    return {
      discardcard: '',
      error: '',
    }
  },
  computed: {
    ...mapState(['username', 'opponent', 'hand', 'topDiscard', 'turn', 'phase'])
  },
  methods: {
    draw(pile) {
      this.$store.dispatch('draw', pile);
    },
    discard(card) {
      this.$store.dispatch('discard', card);
      this.selected = '';
    }
  }
}
</script>

<style>
.card {
  font-size: 24px;
  font-weight: bold;
  margin: 4px;
}
.selected {
  background-color: #ffff88;
}
</style>
