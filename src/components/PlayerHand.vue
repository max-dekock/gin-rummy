<template>
    <card-sequence
        :cards="hand"
        :selected="selectedCards"
        :disabled="disabledCards"
        :selected-color="selectedColor"
        @card-clicked="onClick"
    ></card-sequence>
</template>

<script>
import CardSequence from './CardSequence.vue'
import { isValidCard } from '../rummy_utils.js'

export default {
    name: 'player-hand',
    components: {
        CardSequence,
    },
    model: {
        prop: 'selectedCards',
        event: 'change-selected',
    },
    props: {
        hand: {
            type: Array,
            required: true,
            validator: (value) => value.every(c => isValidCard(c))
        },
        selectedCards: {
            type: Array,
            required: false,
            default: () => [],
            validator: (value) => value.every(c => isValidCard(c))
        },
        disabledCards: {
            type: Array,
            required: false,
            default: () => [],
            validator: (value) => value.every(c => isValidCard(c))
        },
        selectMode: {
            type: String,
            required: false,
            default: 'off',
            validator: (value) => ['off', 'single', 'multi'].includes(value)
        },
        selectedColor: {
            type: String,
            required: false,
            default: 'yellow'
        }
    },
    methods: {
        onClick(card) {
            switch (this.selectMode) {
                case 'single': {
                    if (this.selectedCards.includes(card)) {
                        this.$emit('change-selected', []);
                    } else {
                        this.$emit('change-selected', [card]);
                    }
                    break;
                }
                case 'multi': {
                    let i = this.selectedCards.indexOf(card);
                    if (i == -1) {
                        this.$emit('change-selected', [...this.selectedCards, card]);
                    } else {
                        this.$emit('change-selected', this.selectedCards.filter((value, index) => index != i));
                    }
                    break;
                }
                case 'off':
                default: {
                    this.$emit('card-clicked', card);
                    break; 
                }
            }
        },
        clearSelection() {
            this.$emit('change-selected', []);
        },
    },
    watch: {
        selectMode: function (newVal) {
            if (newVal == 'off' && this.selectedCards.length != 0) {
                this.$emit('change-selected', []);
            } else if (newVal == 'single' && this.selectedCards.length > 1) {
                this.$emit('change-selected', []);
            }
        },
        disabledCards: function (newVal) {
            if (newVal.length > 0) {
                let disabledSet = new Set(newVal);
                let newSelected = this.selectedCards.filter(c => !disabledSet.has(c));
                this.$emit('change-selected', newSelected);
            }
        }
    }
}
</script>