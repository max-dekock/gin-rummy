<template>
  <div class="hand">
    <Card
      v-for="card in cards"
      :card="card"
      :class="[{'selected': selected.includes(card)}, {'disabled': disabled.includes(card)}]"
      :style="{ 'outline-color': selectColor }"
      :key="card"
      @click.native="click(card)"></Card>
  </div>
</template>

<script>
import Card from './Card.vue'

export default {
  model: {
    prop: 'selected',
    event: 'select'
  },
  props: {
    cards: Array,
    selected: {
      type: Array,
      default: () => { return []; },
    },
    selectMode: {
      type: String,
      default: "off",
    },
    selectColor: {
      type: String,
      default: "yellow",
    },
    disabled: {
      type: Array,
      default: () => { return []; },
    },
  },
  methods: {
    click(card) {
      if (this.selectMode == "off") {
        return;
      }
      if (this.disabled.includes(card)) {
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
      this.$emit('select', newsel);
    },
  },
  components: {
    Card
  }
}
</script>

<style>
.hand {
  display: flex;
  flex-wrap: wrap;
  max-width: 80%;
  margin: auto;
}
.selected {
  outline: 2px solid yellow;
}
.disabled {
  color: #222222;
  background-color: #bbbbbb;
  outline-color: #222222;
}
</style>
