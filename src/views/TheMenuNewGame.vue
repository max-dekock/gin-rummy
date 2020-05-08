<template>
  <div>
    <div v-if="joinCode">
        <h2>Game created -- waiting for opponent</h2>
        <h2>Join code: {{joinCode}}</h2>
        <input type="text" :value="joinUrl" id="joinUrl" readonly><button @click="copyUrl">📋</button>
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
        joinUrl() {
            return window.location.origin + this.$router.resolve({path: 'join', query: {code: this.joinCode}}).href;
        }
    },
    methods: {
        newGame() {
            this.$socket.client.emit('newGame', {nickname: this.uname})
        },
        copyUrl() {
            const input = document.getElementById("joinUrl");
            input.focus();
            input.setSelectionRange(0, 999999);
            document.execCommand("copy");
        }
    }
}
</script>

<style scoped>
#joinUrl {
    width: 22em;
    font-size: 16px;
    border: solid 2px gray;
}
</style>