<template>
    <div class="game-wrapper">
        <card-sequence
            class="opponent-hand"
            v-if="!gameFinished && !(turn && phase == 'lay')"
            :cards="opponentHand"
            :options="{faceDown: true}"
        ></card-sequence>
        <div v-else class="opponent-melds">
            <h4 v-if="opponentMelds.length > 0">Melds:</h4>
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
                    class="opponent-melds__layoff"
                ></card-sequence>
            </div>
            <h4 v-if="opponentDeadwood.length > 0">Deadwood:</h4>
            <card-sequence
                v-if="opponentDeadwood.length > 0"
                :cards="opponentDeadwood"
                class="opponent-melds__deadwood"
            ></card-sequence>
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

        <div class="game-score" v-if="gameFinished">
            <h3>Score:</h3>
            <h2>{{nickname}}: {{score.you}} | {{opponent}}: {{score.opponent}}</h2>
        </div>
        <p class="game-wait" v-else-if="uiMode == 'wait'">{{ opponent }}'s turn</p>
        <component v-else class="game-controls" :is="controlsComponent"></component>

        <player-hand v-if="!gameFinished && !(!turn && phase == 'lay')"></player-hand>
        <div v-else class="player-melds">
            <h4 v-if="playerMelds.length > 0">Melds:</h4>
            <div
                v-for="(meld, index) in playerMelds"
                :key="index"
                class="player-melds__wrapper"
            >
                <card-sequence
                    :cards="meld"
                    class="player-melds__meld"
                ></card-sequence>
                <card-sequence
                    v-if="opponentLayoffsOf(index)"
                    :cards="opponentLayoffsOf(index)"
                ></card-sequence>
            </div>
            <!-- TODO: add player meld -->
            <h4 v-if="playerDeadwood.length > 0">Deadwood:</h4>
            <card-sequence
                v-if="playerDeadwood.length > 0"
                :cards="playerDeadwood"
                class="player-melds__deadwood"
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
            score: state => state.gameData.score,
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
                return [];
            }
        },
        playerDeadwood() {
            if ('result' in this.gameData && 'deadwood' in this.gameData.result) {
                return this.gameData.result.deadwood.you;
            } else {
                return [];
            }
        },
        opponentMelds() {
            if ('result' in this.gameData && 'melds' in this.gameData.result) {
                return this.gameData.result.melds.opponent;
            } else {
                return [];
            }
        },
        opponentDeadwood() {
            if ('result' in this.gameData && 'deadwood' in this.gameData.result) {
                return this.gameData.result.deadwood.opponent;
            } else {
                return [];
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
        opponentLayoffs() {
            if ('opponent' in this.$store.getters.layoffs) {
                return this.$store.getters.layoffs.opponent
            } else {
                return [];
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
        opponentLayoffsOf(meldIndex) {
            let lo = [];
            for (let ll of this.opponentLayoffs) {
                if (ll[0] == meldIndex) {
                    lo.push(...ll[1]);
                }
            }
            if (lo.length > 0) {
                return lo;
            } else {
                return null;
            }
            
        }
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
.player-melds__wrapper,.opponent-melds__wrapper {
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