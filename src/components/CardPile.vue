<template>
    <div
        class="card-pile"
        :class="{ clickable: clickable }"
        @click="clickPile"
    >
        <label>{{ label }}</label>
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'card-pile',
    props: {
        clickable: {
            type: Boolean,
            required: false,
            default: false,
        },
        label: {
            type: String,
            required: false,
            default: ''
        }
    },
    methods: {
        clickPile() {
            if (this.clickable) {
                this.$emit('pile-clicked');
            }
        }
    }
}
</script>

<style scoped>
.card-pile {
    display: flex;
    flex-flow: column nowrap;
    justify-items: center;
    align-items: center;
    background-color: #2c3e50;
    padding: 20px;
    margin: 0 30px;
    border: solid 4px #888888;
    border-radius: 12px;
}
.clickable {
    border: solid 4px #34c6eb;
    border-radius: 8px;
}
.clickable:hover {
    border-color: yellow;
}
</style>