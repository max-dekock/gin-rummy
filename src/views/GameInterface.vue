<template>
    <div>
        <div class="header">
            
        </div>

        <div class="opponent-box">
            <h2 class="opponent-name">{{ opponent }}</h2>
            <card-sequence
                class="opponent-hand"
                v-if="!melds.opponent"
                :cards="opponentHand"
                faceDown
            ></card-sequence>
            <deadwood
                class="opponent-deadwood"
                v-else
                :cards="deadwood.opponent"
            ></deadwood>
        </div>

        <div class="board">
            <meld-sequence
                class="opponent-melds"
                v-if="finished && melds.opponent || phase == 'lay' && turn && gin"
                :melds="melds.opponent"
                :layoffs="layoffs.you"
            ></meld-sequence>
            <layoff-select
                class="opponent-melds"
                v-else-if="phase == 'lay' && turn && !gin"
                :melds="melds.opponent"
                :selected="selectedCards"
                v-model="selectedLayoffs"
            ></layoff-select>

            <div style="display:flex; flex-flow:row wrap; justify-items:space-evenly;">
                <card-pile
                    :clickable="mode == 'draw' && !firstTurnDraw"
                    label="Stock pile"
                    @pile-clicked="drawStock"
                >
                    <card faceDown></card>
                </card-pile>

                <card-pile
                    :clickable="mode == 'draw'"
                    label="Discard pile"
                    @pile-clicked="drawDiscards"
                >
                    <card v-if="topDiscard" :card="topDiscard"></card>
                    <card v-else faceDown style="opacity:0;"></card>
                </card-pile>

                <div class="score" v-if="finished">
                    <h2>Score:</h2>
                    <h2>{{nickname}}: {{score.you}} | {{opponent}}: {{score.opponent}}</h2>
                </div>

                <div v-else>
                    <h3>{{ currentPlayer }}'s turn</h3>

                    <button
                        v-if="mode == 'draw' && firstTurnDraw"
                        @click="drawPass"
                    >Pass</button>

                    <button
                        v-if="mode == 'discard'"
                        @click="discard"
                        :disabled="selectedCards.length != 1"
                    >Discard</button>
                    <button
                        v-if="mode == 'discard'"
                        @click="toggleKnockMode"
                    >Knock...</button>
                </div>
            </div>

            <meld-sequence
                class="player-melds"
                v-if="melds.you"
                :melds="melds.you"
                :layoffs="layoffs.opponent ? layoffs.opponent : []"
            ></meld-sequence>
            <template v-else-if="['knock', 'lay'].includes(mode)">
                <meld-select
                    class="player-melds"
                    v-model="selectedMelds"
                    :selected="selectedCards"
                ></meld-select>
                <h3>Deadwood: {{ selectedDeadwoodPoints }}</h3>
                <div>
                    <button v-if="mode == 'knock'" @click="toggleKnockMode">Cancel</button>
                    <button :disabled="!validMeldSelected" @click="addMeld">Add meld</button>
                    <button @click="resetMelds">Reset</button>
                    <button :disabled="mode == 'knock' && !validKnockSelected" @click="submit">Submit</button>
                </div>
            </template>
        </div>

        <div class="player-box">
            <h2 class="player-name">{{ nickname }}</h2>
            <div v-if="!melds.you">
                <player-hand
                    :hand="orderedHand"
                    v-model="selectedCards"
                    :disabledCards="disabledCards"
                    :selectMode="handSelectMode"
                    :selectedColr="handSelectedColor"
                ></player-hand>
                <reorder-controls
                    :arr="hand"
                    v-model="orderedHand"
                    :selectedIndices="selectedCards.map(c => orderedHand.indexOf(c))"
                ></reorder-controls>
                <button @click="sortHand">Sort</button>
                <button @click="clearSelection">Clear</button>
            </div>
            <deadwood v-else :cards="deadwood.you"></deadwood>
        </div>
    </div>
</template>

<script>
import Card from '../components/Card.vue'
import CardSequence from '../components/CardSequence.vue'
import PlayerHand from '../components/PlayerHand.vue'
import ReorderControls from '../components/ReorderControls.vue'
import CardPile from '../components/CardPile.vue'
import MeldSequence from '../components/MeldSequence.vue'
import MeldSelect from '../components/MeldSelect.vue'
import LayoffSelect from '../components/LayoffSelect.vue'
import Deadwood from '../components/Deadwood.vue'

import { mapState, mapGetters, mapActions } from 'vuex'

import { pointValue, deadwoodPoints, compareCards, isMeld } from '../rummy_utils.js'

export default {
    name: 'game-interface',
    components: {
        Card,
        CardSequence,
        PlayerHand,
        ReorderControls,
        CardPile,
        MeldSequence,
        MeldSelect,
        LayoffSelect,
        Deadwood
    },
    data() {
        return {
            orderedHand: [],
            selectedCards: [],
            selectedMelds: [],
            selectedLayoffs: [],
            knockMode: false,
        };
    },
    computed: {
        ...mapState('gameState', [
            'started',
            'finished',
            'nickname',
            'opponent',
            'turn',
            'phase',
            'topDiscard',
            'hand',
            'firstTurnDraw',
            'knocker',
            'melds',
            'layoffs',
            'deadwood',
            'score',
        ]),
        ...mapGetters('gameState', [
            'currentPlayer',
            'gin',
            'undercut',
            'winner',
        ]),
        mode() {
            if (!this.started) {
                return 'unstarted';
            } else if (this.finished) {
                return 'finished';
            } else if (!this.turn) {
                return 'wait';
            } else if (this.phase == 'draw') {
                return 'draw'
            } else if (this.phase == 'discard') {
                return this.knockMode ? 'knock' : 'discard';
            } else if (this.phase == 'lay') {
                return 'lay';
            } else {
                console.warn('Illegal GameInterface mode');
                return 'illegal';
            }
        },
        opponentHand() {
            let hand;
            if (this.turn == false && this.phase == 'discard') {
                hand = new Array(11);
            } else {
                hand = new Array(10);
            }
            hand.fill('??');
            return hand;
        },
        knockDiscard() {
            if (this.mode != 'knock') {
                return null;
            }
            let deadwood = new Set(this.hand);
            for (let meld of this.selectedMelds) {
                meld.forEach(c => deadwood.delete(c));
            }
            if (deadwood.size == 0) {
                return '';
            } else {
                let darr = Array.from(deadwood);
                darr.sort((c1, c2) => pointValue(c2) - pointValue(c1));
                return darr[0];
            }
        },
        selectedDeadwood() {
            let deadwood = new Set(this.hand);
            this.selectedMelds.forEach(
                meld => meld.forEach(
                    card => deadwood.delete(card)
            ));
            if (this.mode == 'knock') {
                deadwood.delete(this.knockDiscard);
            } else if (this.mode == 'lay') {
                this.selectedLayoffs.forEach(
                    layoff => layoff.forEach(
                        card => deadwood.delete(card)
                ));
            }
            return Array.from(deadwood);
        },
        selectedDeadwoodPoints() {
            return deadwoodPoints(this.selectedDeadwood);
        },
        validMeldSelected() {
            return isMeld(this.selectedCards);
        },
        validKnockSelected() {
            return this.selectedDeadwoodPoints <= 10;
        },
        disabledCards() {
            let disabled = [];
            if (this.mode == 'knock' || this.mode == 'lay') {
                this.selectedMelds.forEach(
                    meld => meld.forEach(
                        card => disabled.push(card)
                ));
            }
            if (this.mode == 'lay') {
                this.selectedLayoffs.forEach(
                    layoff => layoff.forEach(
                        card => disabled.push(card)
                ));
            }
            return disabled;
        },
        handSelectMode() {
            switch (this.mode) {
                case 'discard':
                    return 'single';
                case 'wait':
                case 'draw':
                case 'knock':
                case 'lay':
                    return 'multi';
                default:
                    return 'off';
            }
        },
        handSelectedColor() {
            if (this.mode == 'knock' || this.mode == 'lay') {
                return this.validMeldSelected ? 'limegreen' : 'red';
            } else {
                return 'yellow';
            }
        }
    },
    methods: {
        ...mapActions({
            drawStock: dispatch => dispatch('draw', 'stock'),
            drawDiscards: dispatch => dispatch('draw', 'discards'),
            drawPass: dispatch => dispatch('draw', 'refuse'),
        }),
        discard() {
            if (this.selectedCards.length == 1) {
                this.$store.dispatch('discard', this.selectedCards[0]);
                this.selectedCards = [];
            }
        },
        knock() {
            this.$store.dispatch('knock', {
                melds: this.selectedMelds,
                discard: this.knockDiscard,
                deadwood: this.selectedDeadwood,
            });
        },
        lay() {
            this.$store.dispatch('lay', {
                melds: this.selectedMelds,
                layoffs: this.selectedLayoffs,
            });
        },
        clearSelection() {
            this.selectedCards = [];
        },
        sortHand() {
            this.orderedHand.sort(compareCards);
        },
        toggleKnockMode() {
            this.knockMode = !this.knockMode;
        },
        addMeld() {
            if (!this.validMeldSelected) {
                console.warn('Tried to add invalid meld');
                return;
            }
            this.selectedMelds.push(Array.from(this.selectedCards).sort(compareCards));
        },
        resetMelds() {
            this.selectedMelds = [];
        },
        submit() {
            if (this.mode == 'knock') {
                this.knock();
            } else if (this.mode == 'lay') {
                this.lay();
            }
        },

    }
}
</script>

<style>
.player-box,.opponent-box {
    display: flex;
    flex-flow: column nowrap;
    align-items: center;
    background-color: #1c1627;
    padding: 20px;
    margin: 30px;
    border: solid 4px #444444;
    border-radius: 12px;
}
.player-name,.opponent-name {
    margin: 0;
}
</style>