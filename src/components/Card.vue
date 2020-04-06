<template>
  <div
    class="card"
    :class="{'card-back': faceDown}"
    :style="{'color': suitColor}"
    @click="$emit('card-clicked', card)"
  >{{ content }}</div>
</template>

<script>
export default {
  props: {
    card: String,
    useUnicodeSuits: {
      type: Boolean,
      default: true
    },
    faceDown: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    content() {
      if (this.faceDown) {
        return '\u2020';
      } else {
        return this.rank + this.suit;
      }
    },
    rank() {
      if (this.faceDown) {
        return undefined;
      }
      return this.card.charAt(0);
    },
    suit() {
      if (this.faceDown) {
        return undefined;
      }
      if (this.useUnicodeSuits) {
        switch(this.card.charAt(1).toLowerCase()) {
          case 's':
            return '\u2660';
          case 'h':
            return '\u2665';
          case 'd':
            return '\u2666';
          case 'c':
            return '\u2663';
        }
      }
      return this.card.charAt(1);
    },
    suitColor() {
      if (this.faceDown) {
        return 'black';
      }
      switch(this.card.charAt(1)) {
        case 's':
        case 'c':
          return 'var(--suit-black)';
        case 'h':
        case 'd':
          return 'var(--suit-red)';
        default:
          return 'inherit';
      }
    }
  }
}
</script>

<style>
.card {
  --suit-black: black;
  --suit-red: #dd0000;
  font-size: 24px;
  font-weight: bold;
  width: 2.5ch;
  height: 3.5ch;
  margin: 4px;
  padding: 4px;
  color: black;
  background-color: white;
  border: 2px solid white;
}

.card-back {
  background-color: #be67e6;
}
</style>
