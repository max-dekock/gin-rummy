<template>
    <div>
        <meld-sequence
            :melds="melds"
            v-slot:meld-postfix="meld"
        >
            <button
                @click="removeMeld(meld.index)"
            >🗙</button> <!-- 🗙 (U+1F5D9 CANCELLATION X) -->
            <h1>☉</h1>
            <button
                @click="addLayoff(meld.index)"
                :disabled="!validLayoffSelected(meld.index)"
            >＋</button>
            <span
                v-if="layoffs[meld.index] 
                   && layoffs[meld.index].length > 0"
                style="display: flex;"
            >
                <card-sequence
                    :cards="layoffs[meld.index]"
                ></card-sequence>
                <button
                    @click="removeLayoff(meld.index)"
                >🗙</button>
            </span>
        </meld-sequence>

        <div v-if="discard" class="discard-wrapper">
            Discard:
            <card :card="discard" class="discard-wrapper__card"></card>
            <button @click="removeDiscard" class="discard-wrapper__remove">&#x1f5d9;</button>
        </div>

        <div>
            <button
                @click="addMeld"
                :disabled="!validMeldSelected"
            >Add meld</button>
            <button
                @click="addDiscard"
                :disabled="discard || selected.length != 1"
            >Add discard</button>
            <button
                @click="reset"
            >Reset</button>
            <button
                @click="submit"
                :disabled="!validKnockSelected"
            >Submit</button>
        </div>

        <player-hand
            v-model="selected"
            :hand="orderedHand"
            :disabledCards="disabledCards"
            :selectedColor="selectedColor"
            selectMode="multi"
        ></player-hand>
        <reorder-controls
            :arr="hand"
            v-model="orderedHand"
            :selected-indices="selectedIndices"
        ></reorder-controls>
        <div>
            <button @click="sortHand">Sort</button>
            <button @click="reverseHand">Reverse</button>
            <button @click="shuffleHand">Shuffle</button>
        </div>
        <div>
            <button @click="selected = []">Clear selection</button>
            <button @click="orderedHand = hand">Reset order</button>
        </div>
    </div>
</template>

<script>
import { DECK, isMeld, compareCards, shuffle } from '../rummy_utils.js'
import MeldSequence from '../components/MeldSequence.vue'
import Card from '../components/Card.vue'
import PlayerHand from '../components/PlayerHand2.vue'
import ReorderControls from '../components/ReorderControls.vue'
import CardSequence from '../components/CardSequence2.vue'

export default {
    name: 'meld-test',
    components: {
        MeldSequence,
        Card,
        PlayerHand,
        ReorderControls,
        CardSequence
    },
    data() {
        return {
            hand: DECK,
            orderedHand: [],
            melds: [],
            layoffs: [],
            discard: '',
            selected: []
        };
    },
    computed: {
        selectedIndices() {
            return this.selected.map(c => this.orderedHand.indexOf(c));
        },
        validMeldSelected() {
            return isMeld(this.selected);
        },
        validKnockSelected() {
            return true;
        },
        disabledCards() {
            let dc = [...this.melds.flat(), ...this.layoffs.flat()];
            if (this.discard) {
                dc.push(this.discard);
            }
            return dc;
        },
        selectedColor() {
            if (this.validMeldSelected) {
                return 'limegreen';
            } else {
                return 'orange';
            }
        }
    },
    methods: {
        addMeld() {
            if (!this.validMeldSelected) {
                console.warn(`Tried to add invalid meld ${this.selected.join(' ')}`);
                return;
            }
            this.melds.push(Array.from(this.selected));
            this.melds[this.melds.length - 1].sort(compareCards);
            this.selected = [];
        },
        removeMeld(i) {
            if (!(i in this.melds)) {
                console.warn(`Tried to remove non-existent meld at index ${i}`);
                return;
            }
            this.melds.splice(i, 1);
            this.layoffs.splice(i, 1);
        },
        validLayoffSelected(i) {
            if (!(i in this.melds)) {
                return false;
            }
            if (this.selected.length <= 0) {
                return false;
            }
            let m = this.melds[i].concat(this.selected);
            if (this.layoffs[i]) {
                m.push(...this.layoffs[i]);
            }
            return isMeld(m);
        },
        addLayoff(i) {
            if (!this.validLayoffSelected(i)) {
                console.warn(`Tried to add invalid layoff at index ${i}`);
                return;
            }
            if (!this.layoffs[i]) this.layoffs.splice(i, 1, []);
            this.layoffs[i].push(...this.selected);
            this.layoffs[i].sort(compareCards);
            this.selected = [];
        },
        removeLayoff(i) {
            this.layoffs.splice(i, 1, []);
        },
        addDiscard() {
            if (this.discard) {
                console.warn('Tried to add discard when discard already selected');
                return;
            }
            if (this.selected.length != 1) {
                console.warn('Tried to add discard when number of selected cards not equal to 1');
                return;
            }
            this.discard = this.selected[0];
            this.selected = [];
        },
        removeDiscard() {
            if (!this.discard) {
                console.warn('Tried to remove non-existent discard');
                return;
            }
            this.discard = '';
        },
        reset() {
            this.melds = [];
            this.discard = '';
            this.selected = [];
            this.layoffs = [];
        },
        submit() {
            if (!this.validKnockSelected) {
                console.warn('Tried to submit invalid knock');
                return;
            }
            console.log('Melds:');
            for (let meld of this.melds) {
                console.log(`\t${meld.join(' ')}`);
            }
            console.log(`Discard:\n\t${this.discard}`);
        },
        sortHand() {
            this.orderedHand.sort(compareCards);
        },
        reverseHand() {
            this.orderedHand.reverse();
        },
        shuffleHand() {
            let a = Array.from(this.orderedHand);
            shuffle(a);
            this.orderedHand = a;
        }
    }
}
</script>

<style scoped>
.discard-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>