<template>
  <div>
    <div v-if="joinCode">
        <h2>Game created -- waiting for opponent</h2>
        <h2>Join code: {{joinCode}}</h2>
    </div>
    <div v-else>
        <label>Nickname: <input type="text" v-model="uname"></label>
        <button @click="newGame">New game</button>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    data() {
        return {
            uname: '',
        };
    },
    computed: {
        ...mapState(['joinCode']),
    },
    methods: {
        newGame() {
            this.$socket.client.emit('newGame', {nickname: this.uname})
        }
    }
}
</script>