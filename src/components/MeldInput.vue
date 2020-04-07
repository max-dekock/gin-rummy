<template>
    <div class="meld-input">
        <div v-for="mkey in mkeys"
            class="meld-input__meld-wrapper"
            :key="mkey"
        >
            <button class="removeMeldButton" @click="removeMeld(mkey)">Remove</button>
            <card-sequence :cards="meld(mkey)"></card-sequence>
        </div>
    </div>
</template>

<script>
import CardSequence from './CardSequence.vue'

export default {
    name: 'meld-input',
    components: {
        CardSequence,
    },
    model: {
        prop: 'melds',
        event: 'updateMelds'
    },
    props: {
        melds: {
            type: Array,
            default: () => [],
        }
    },
    computed: {
        mkeys() {
            return this.melds.keys();
        }
    },
    methods: {
        meld(mkey) {
            return this.melds[mkey];
        },
        removeMeld(mkey) {
            let newMelds = Array.from(this.melds);
            newMelds.splice(mkey, 1);
            this.$emit('updateMelds', newMelds);
        }
    }
}
</script>

<style scoped>
.meld-input__meld-wrapper {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}
</style>