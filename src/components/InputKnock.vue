<template>
    <div class="knock">
        <div>
            <MeldInput v-model="melds"></MeldInput>
            <Card v-if="discard" :card="discard"></Card>
            <p>Deadwood count: {{ deadwoodPoints }}</p>
        </div>
        <div>
            <button @click="cancelKnock">Cancel</button>
            <button @click="resetKnock">Reset</button>
            <button @click="knock" :disabled="!knockValid">Knock</button>
            <button @click="addMeld" :disabled="!meldSelected">Add meld</button>
            <button v-if="!discard" @click="setDiscard" :disabled="selectedCards.length != 1">Add discard</button>
            <button v-else @click="clearDiscard">Clear discard</button>
        </div>
    </div>
</template>

<script>
import Card from './Card.vue'
import MeldInput from './MeldInput.vue'
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

export default {
    name: 'input-knock',
    components: {
        Card,
        MeldInput
    },
    computed: {
        ...mapState({
            discard: state => state.ui.knockDiscard,
            selectedCards: state => state.ui.selectedCards,
        }),
        ...mapGetters(['deadwoodPoints', 'meldSelected', 'knockValid']),
        melds: {
            get () {
                return this.$store.state.ui.melds;
            },
            set(value) {
                this.$store.commit('updateUI', {melds: value});
            }
        }
    },
    methods: {
        ...mapMutations({
            cancelKnock: 'resetUI',
            resetKnock: commit => commit('updateUI', {melds: [], knockDiscard: '', selectedCards: []}),
            clearDiscard: commit => commit('updateUI', {knockDiscard: ''}),
        }),
        ...mapActions(['addMeld', 'removeMeld', 'knock']),
        setDiscard() {
            if (this.selectedCards.length == 1) {
                this.$store.commit('updateUI', {knockDiscard: this.selectedCards[0]})
            } else {
                console.warn('KnockInput: tried to set discard with multiple cards selected');
            }
        }
    }
}
</script>