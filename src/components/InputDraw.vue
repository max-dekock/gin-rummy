<template>
    <div class="input-draw">
        <button
            v-if="!firstTurnDraw"
            @click="draw('stock')"
        >Draw from Stock</button>
        <button
            @click="draw('discards')"
        >Draw from Discards</button>
        <button
            v-if="firstTurnDraw"
            @click="draw('refuse')"
        >Pass</button>
    </div>
</template>

<script>
export default {
    name: 'input-draw',
    computed: {
        firstTurnDraw() {
            return this.$store.state.gameData.firstTurnDraw;
        }
    },
    methods: {
        draw(pile) {
            this.$store.dispatch('draw', pile);
        }
    }
}
</script>