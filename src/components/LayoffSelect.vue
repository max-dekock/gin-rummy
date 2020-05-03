<template>
    <meld-sequence
        :melds="sortedMelds"
        :layoffs="sortedLayoffs"
    >
        <template #meld-postfix="meld">
            <button
                @click="addLayoff(meld.index)"
                :disabled="!validLayoffSelected(meld.index)"
            >Add</button>
            <button
                @click="clearLayoff(meld.index)"
                v-if="meld.layoff && meld.layoff.length > 0"
            >Clear</button>
        </template>
    </meld-sequence>
</template>

<script>
import MeldSequence from './MeldSequence.vue'
import { isMeld, compareCards } from '../rummy_utils.js'

export default {
    name: 'layoff-select',
    components: {
        MeldSequence
    },
    model: {
        prop: 'layoffs',
        event: 'change-layoffs'
    },
    props: {
        melds: {
            type: Array,
            required: true,
        },
        layoffs: {
            type: Array,
            required: true,
        },
        selected: {
            type: Array,
            required: true
        }
    },
    computed: {
        sortedMelds() {
            return this.melds.map(meld => {
                let sorted = Array.from(meld);
                sorted.sort(compareCards);
                return sorted;
            });
        },
        sortedLayoffs() {
            return this.layoffs.map(layoff => {
                let sorted = Array.from(layoff);
                sorted.sort(compareCards);
                return sorted;
            });
        },
    },
    methods: {
        validLayoffSelected(i) {
            if (this.selected.length <= 0) {
                return false;
            }
            if (!(i in this.melds)) {
                return false;
            }
            let cards = this.melds[i].concat(this.selected);
            if (i in this.layoffs) {
                cards.push(...this.layoffs[i]);
            }
            return isMeld(cards);
        },
        addLayoff(i) {
            if (!this.validLayoffSelected(i)) {
                console.warn(`Tried to add invalid layoff at index ${i}`);
                return;
            }
            let newLayoffs = Array.from(this.layoffs);
            if (newLayoffs[i] === undefined) {
                newLayoffs[i] = [];
            }
            newLayoffs[i].push(...this.selected);
            this.$emit('change-layoffs', newLayoffs);
        },
        clearLayoff(i) {
            if (!(i in this.layoffs)) {
                return;
            }
            let newLayoffs = Array.from(this.layoffs)
            newLayoffs.splice(i, 1, []);
            this.$emit('change-layoffs', newLayoffs);
        }
    }
}
</script>