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
        selected: {
            type: Array,
            required: false,
            default: () => [],
        },
        disabled: {
            type: Array,
            required: false,
            default: () => [],
        },
        selectedColor: {
            type: String,
            required: false,
            default: 'yellow'
        },
        faceDown: {
            type: Boolean,
            required: false,
            default: false
        }
    },
    computed: {
        seq() {
            let s = [];
            for (let i in this.cards) {
                s.push(this.cObj(i));
            }
            return s;
        },
        selectedSet() {
            return new Set(this.selected);
        },
        disabledSet() {
            return new Set(this.disabled);
        }
    },
    methods: {
        onClick(card) {
            if (!this.disabledSet.has(card)) {
                this.$emit('card-clicked', card);
            }
        },
        cObj(i) {
            if (this.faceDown) {
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
                if (this.selectedSet.has(card)) {
                    cl.selected = true;
                    st['outline-color'] = this.selectedColor;
                }
                if (this.disabledSet.has(card)) {
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
  outline: 2px solid;
  outline-offset: 2px;
}
.disabled {
  background-color: #bbbbbb;
  border-color: #555555;
}
.card-sequence {
    display: flex;
    flex-wrap: wrap;
}
</style>