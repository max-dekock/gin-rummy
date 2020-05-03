<template>
    <div class="seq">
        <div
            class="wrapper"
            v-for="(meld, index) of melds"
            :key="index"
        >
            <slot
                class="wrapper__prefix"
                name="meld-prefix"
                :cards="meld"
                :index="index"
                :layoff="layoffs[index]"
            ></slot>
            <card-sequence
                class="wrapper__meld"
                :cards="meld"
            ></card-sequence>
            <card-sequence
                class="wrapper__layoff"
                v-if="layoffs[index]"
                :cards="layoffs[index]"
            ></card-sequence>
            <slot
                class="wrapper__postfix"
                name="meld-postfix"
                :cards="meld"
                :index="index"
                :layoff="layoffs[index]"
            ></slot>
        </div>
    </div>
</template>

<script>
import CardSequence from './CardSequence2.vue'

export default {
    name: 'meld-sequence',
    components: {
        CardSequence
    },
    props: {
        melds: {
            type: Array,
            required: true
        },
        layoffs: {
            type: Array,
            required: false,
            default: () => []
        }
    }
}
</script>

<style scoped>
.wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>