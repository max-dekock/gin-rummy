<template>
  <div>
    <label>Username: <input type="text" v-model="uname"></label>
    <button @click="createGame">Create game</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      uname: ''
    };
  },
  methods: {
    createGame() {
      this.$socket.client.emit('newGame', {username:this.uname});
    }
  },
  sockets: {
    join() {
      this.$router.push('/game');
    }
  }
}
</script>
