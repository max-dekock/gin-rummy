<template>
    <div>
        <slot
            :reposition="reposition"
            :shiftSelected="shiftSelected"
            :canShift="canShift"
        >
            <div>
                <button
                    @click="shiftSelected(-Infinity)"
                    :disabled="!canShift(-Infinity)"
                >⭰</button>
                <button
                    @click="shiftSelected(indicesSequential ? -1 : -0)"
                    :disabled="!canShift(-1)"
                >⭠</button>
                <button
                    @click="shiftSelected(indicesSequential ? +1 : +0)"
                    :disabled="!canShift(1)"
                >⭢</button>
                <button
                    @click="shiftSelected(+Infinity)"
                    :disabled="!canShift(Infinity)"
                >⭲</button>
            </div>
        </slot>
    </div>
</template>

<script>
import { repositioned, updated } from '../reorder.js'

export default {
    name: 'reorder-controls',
    model: {
        prop: 'orderedArr',
        event: 'change-order'
    },
    props: {
        arr: {
            type: Array,
            required: true
        },
        orderedArr: {
            type: Array,
            required: false,
            default: () => []
        },
        selectedIndices: {
            type: Array,
            required: false,
            default: () => []
        }
    },
    computed: {
        indicesSequential() {
            return Math.max(...this.selectedIndices) 
                 - Math.min(...this.selectedIndices)
                 + 1
                == this.selectedIndices.length;
        }
    },
    watch: {
        arr: {
            immediate: true,
            handler(newArr) {
                this.$emit('change-order', updated(this.orderedArr, newArr));
            }
        }
    },
    methods: {
        reposition(indices, offset) {
            this.$emit('change-order', repositioned(this.orderedArr, indices, offset));
        },
        shiftSelected(offset) {
            this.reposition(this.selectedIndices, offset);
        },
        canShift(offset) {
            // Returns true if shiftSelected(offset) will have any effect.
            if (this.selectedIndices.length <= 0) return false;
            if (!this.indicesSequential) return true;

            let negativeOffset = offset < 0 || Object.is(offset, -0);
            return negativeOffset
                ? Math.min(...this.selectedIndices) > 0
                : Math.max(...this.selectedIndices) < this.orderedArr.length - 1;
        }
    }
}
</script>