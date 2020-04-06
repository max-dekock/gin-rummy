<template>
    <div class="input-discard">
        <button
            :disabled="selectedCards.length != 1"
            @click="discard"
        >Discard</button>
        <button
            @click="setKnockMode"
        >Knock...</button>
    </div>
</template>

<script>
export default {
    name: 'input-discard',
    computed: {
        selectedCards() {
            return this.$store.state.ui.selectedCards;
        }
    },
    methods: {
        discard() {
            this.$store.dispatch('discard', this.selectedCards[0]);
        },
        setKnockMode() {
            this.$store.commit('updateUI', {knockMode: true});
        }
    }
}
</script>