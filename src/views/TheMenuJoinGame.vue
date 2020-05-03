<template>
  <div>
    <label>Nickname: <input type="text" v-model="uname"></label>
    <label>Join code: <input type="text" v-model="joinCode"></label>
    <button @click="joinGame">Join game</button>
  </div>
</template>

<script>
export default {
    data() {
        return {
            uname: '',
            joinCode: '',
        };
    },
    methods: {
        joinGame() {
            this.$socket.client.emit('joinGame', {nickname: this.uname, joinCode: this.joinCode})
        }
    },
    mounted() {
        if (this.$route.query.code) {
            this.joinCode = this.$route.query.code;
        }
    }
}
</script>