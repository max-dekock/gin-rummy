<template>
    <meld-sequence :melds="melds">
        <template #meld-postfix="meld">
            <button @click="removeMeld(meld.index)">🗙</button>
        </template>
    </meld-sequence>
</template>

<script>
import MeldSequence from './MeldSequence.vue'

export default {
    name: 'meld-select',
    components: {
        MeldSequence,
    },
    model: {
        prop: 'melds',
        event: 'change-melds'
    },
    props: {
        melds: {
            type: Array,
            required: true
        }
    },
    methods: {
        removeMeld(index) {
            let newMelds = Array.from(this.melds);
            newMelds.splice(index, 1);
            this.$emit('change-melds', newMelds);
        }
    }
}
</script>