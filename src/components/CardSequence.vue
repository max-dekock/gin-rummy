<template>
    <div class="card-sequence">
        <Card
            v-for="c in seq"
            :key="c.id"
            :card="c.card"
            :class="c.class"
            :style="c.style"
            v-bind="c.props"
            @card-clicked="onClick"
        ></Card>
    </div>
</template>

<script>
import Card from './Card.vue'

export default {
    name: 'card-sequence',
    components: {
        Card
    },
    props: {
        cards: {
            type: Array,
            required: true
        },
        options: {
            type: Object,
            default: () => { return {
                selected: new Set(),
                selectedColor: "yellow",
                disabled: new Set(),
                faceDown: false
            } }
        }
    },
    computed: {
        seq() {
            let s = [];
            for (let i in this.cards) {
                s.push(this.cObj(i));
            }
            return s;
        }
    },
    methods: {
        onClick(card) {
            this.$emit('card-clicked', card);
        },
        cObj(i) {
            if (this.options.faceDown) {
                return {
                    id: i,
                    card: '',
                    class: {},
                    style: {},
                    props: { faceDown: true }
                };
            } else {
                let card = this.cards[i]
                let cl = {};
                let st = {};
                let pr = {};
                if (this.options.selected && this.options.selected.has(card)) {
                    cl.selected = true;
                    st['outline-color'] = this.options.selectedColor;
                }
                if (this.options.disabled && this.options.disabled.has(card)) {
                    cl.disabled = true;
                }
                return {
                    id: i,
                    card: card,
                    class: cl,
                    style: st,
                    props: pr
                };
            }
        }
    }
}
</script>

<style scoped>
.selected {
  outline: 2px solid yellow;
  outline-offset: 2px;
}
.disabled {
  color: #555555;
  background-color: #bbbbbb;
  border-color: #555555;
}
.card-sequence {
    display: flex;
    flex-wrap: wrap;
}
</style>