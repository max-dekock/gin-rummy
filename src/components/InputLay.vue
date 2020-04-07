<template>
    <div class="input-lay">
        <div
            v-for="(meld, index) in melds"
            :key="index"
            class="input-lay__meld-wrapper"
        >
            <card-sequence :cards="meld"></card-sequence>
            <button @click="removeMeld(index)">Remove</button>
        </div>
        <div>
            <button @click="reset">Reset</button>
            <button
                @click="addMeld"
                :disabled="!meldSelected"
            >Add meld</button>
            <button @click="submit">Submit</button>
        </div>
    </div>
</template>

<script>
import CardSequence from './CardSequence.vue'
import { mapGetters } from 'vuex'

export default {
    name: 'input-lay',
    components: {
        CardSequence
    },
    computed: {
        melds: {
            get() {
                return this.$store.state.ui.melds;
            },
            set(value) {
                this.$store.commit('updateUI', {melds: value});
            }
        },
        selectedCards:{
            get() {
                return this.$store.state.ui.selectedCards;
            },
            set(value) {
                this.$store.commit('updateUI', {selectedCards: value});
            }
        },
        ...mapGetters([
            'meldSelected',
            'knockValid'
        ])
    },
    methods: {
        submit() {
            this.$store.dispatch('lay');
        },
        reset() {
            this.$store.commit('resetUI');
        },
        addMeld() {
            this.melds.push(this.selectedCards);
            this.selectedCards = [];
        },
        removeMeld(index) {
            this.melds.splice(index, 1);
        }
    }
}
</script>

<style scoped>
.input-lay__meld-wrapper {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}
</style>