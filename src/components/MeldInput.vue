<template>
    <div class="meldInput">
        <div v-for="mkey in mkeys"
            class="meld"
            :key="mkey"
        >
            <button class="removeMeldButton" @click="removeMeld(mkey)">Remove</button>
            <Hand :cards="meld(mkey)"></Hand>
        </div>
    </div>
</template>

<script>
import Hand from './Hand.vue'

export default {
    components: {
        Hand,
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