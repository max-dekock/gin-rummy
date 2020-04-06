<template>
    <div class="game-wrapper">
        <card-sequence
            class="opponent-hand"
            v-if="!opponentMelds"
            :cards="opponentHand"
            :options="{faceDown: true}"
        ></card-sequence>
        <div v-else class="opponent-melds">
            <div
                v-for="(meld, meldIndex) in opponentMelds"
                :key="meldIndex"
                class="opponent-melds__wrapper"
            >
                <card-sequence
                    class="opponent-melds__meld"
                    :cards="meld"
                ></card-sequence>
                <button
                    v-if="layoffsPermitted && !layoffs[meldIndex]"
                    :disabled="!validLayoffs(meldIndex)"
                    @click="addLayoffs(meldIndex)"
                >Lay off</button>
                <card-sequence 
                    v-if="layoffs[meldIndex]"
                    :cards="layoffs[meldIndex]"
                ></card-sequence>
            </div>
        </div>
        <h3 class="opponent-name">{{ opponent }}</h3>

        <div class="stock-pile">
            <Card class="pile-card" faceDown></Card>
            <p>Stock pile</p>
        </div>
        <div class="discards-pile">
            <Card class="pile-card" v-if="topDiscard" :card="topDiscard"></Card>
            <p>Discard pile</p>
        </div>

        <h2 class="game-score" v-if="gameFinished">{{score}}</h2>
        <p class="game-wait" v-else-if="uiMode == 'wait'">{{ opponent }}'s turn</p>
        <component v-else class="game-controls" :is="controlsComponent"></component>

        <player-hand v-if="!playerMelds"></player-hand>
        <div v-else class="player-melds">
            <card-sequence
                v-for="mkey in playerMelds.keys()"
                :key="mkey"
                :cards="playerMelds[mkey]"
                class="player-melds__meld"
            ></card-sequence>
        </div>
        <h3 class="player-name">{{ nickname }}</h3>
    </div>
</template>

<script>
import Card from '../components/Card.vue'
import CardSequence from '../components/CardSequence.vue'
import PlayerHand from '../components/PlayerHand.vue'
import InputDraw from '../components/InputDraw.vue'
import InputDiscard from '../components/InputDiscard.vue'
import InputKnock from '../components/InputKnock.vue'
import InputLay from '../components/InputLay.vue'

import { mapState, mapGetters } from 'vuex'

import { isMeld } from '../rummy_utils.js'

export default {
    name: 'game-interface',
    components: {
        Card,
        CardSequence,
        PlayerHand,
        InputDraw,
        InputDiscard,
        InputKnock,
        InputLay
    },
    computed: {
        ...mapState({
            gameData: 'gameData',
            error: 'error',
            nickname: state => state.gameData.nickname,
            opponent: state => state.gameData.opponent,
            turn: state => state.gameData.turn,
            phase: state => state.gameData.phase,
            hand: state => state.gameData.hand,
            topDiscard: state => state.gameData.topDiscard,
            score: state => state.gameData.score
        }),
        ...mapGetters([
            'uiMode', 'gameFinished'
        ]),
        selectedCards: {
            get() {
                return this.$store.state.ui.selectedCards;
            },
            set(value) {
                this.$store.commit('updateUI', {selectedCards: value});
            }
        },
        layoffs: {
            get() {
                return this.$store.state.ui.layoffs;
            },
            set(value) {
                this.$store.commit('updateUI', {layoffs: value});
            }
        },
        controlsComponent() {
            switch (this.uiMode) {
                case 'draw':
                    return 'InputDraw';
                case 'discard':
                    return 'InputDiscard';
                case 'knock':
                    return 'InputKnock';
                case 'lay':
                    return 'InputLay';
                default:
                    return undefined;
            }
        },
        playerMelds() {
            if ('result' in this.gameData && 'melds' in this.gameData.result) {
                return this.gameData.result.melds.you;
            } else {
                return undefined;
            }
        },
        opponentMelds() {
            if ('result' in this.gameData && 'melds' in this.gameData.result) {
                return this.gameData.result.melds.opponent;
            } else {
                return undefined;
            }
        },
        opponentHand() {
            if (this.turn == false && this.phase == 'discard') {
                let a = new Array(11);
                a.fill('xx');
                return a;
            } else {
                let a = new Array(10);
                a.fill('xx');
                return a;
            }
        },
        layoffsPermitted() {
            return (this.uiMode == 'lay' && !this.gameData.result.gin);
        }        
    },
    methods: {
        addLayoffs(meldIndex) {
            let newLayoffs = [...this.layoffs];
            newLayoffs[meldIndex] = Array.from(this.selectedCards);
            this.layoffs = newLayoffs;
            this.selectedCards = [];
        },
        validLayoffs(meldIndex) {
            if (this.selectedCards.length == 0) { return false; }
            let meld = this.opponentMelds[meldIndex];
            let lo = this.layoffs[meldIndex] ? this.layoffs[meldIndex] : [];
            return isMeld(meld.concat(lo, this.selectedCards));
        },
    }
}
</script>

<style>
.game-wrapper {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-auto-rows: minmax(0px, auto);
    grid-gap: 10px;
}
.opponent-hand,.opponent-melds {
    grid-row: 2;
    grid-column: 2 / 6;
    margin: auto;

}
.opponent-melds__wrapper {
    display: flex;
    flex-wrap: wrap;
}
.opponent-name {
    grid-row: 2;
    grid-column: 1;
    text-align: right;
}
.stock-pile {
    grid-row: 4;
    grid-column: 2;
}
.discards-pile {
    grid-row: 4;
    grid-column: 4;
}
.pile-card {
    margin: auto;
}
.game-score,.game-controls,.game-wait {
    grid-row: 5;
    grid-column: 1 / 6;
}
.player-hand,.player-melds {
    grid-row: 6;
    grid-column: 2 / 6;
    margin: auto;
}
.player-name {
    grid-row: 6;
    grid-column: 1;
    text-align: right;
}
</style>