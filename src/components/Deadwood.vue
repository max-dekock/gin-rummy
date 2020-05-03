<template>
    <div class="deadwood" style="display:flex; flex-flow:row nowrap;">
        <h4>Deadwood:</h4>
        <card-sequence
            :cards="cards"
        ></card-sequence>
        <h4>{{ deadwoodPoints }} points</h4>
    </div>
</template>

<script>
import CardSequence from './CardSequence2.vue'
import { deadwoodPoints } from '../rummy_utils.js'

export default {
    name: 'deadwood',
    components: {
        CardSequence,
    },
    props: {
        cards: {
            type: Array,
            required: true
        }
    },
    computed: {
        deadwoodPoints() {
            return deadwoodPoints(this.cards);
        }
    }
}
</script>

<style scoped>
.deadwood {
    display: flex;
    flex-flow: row wrap;
}
</style>