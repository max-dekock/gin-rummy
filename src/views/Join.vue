<template>
  <div>
    <label>Username: <input type="text" v-model="uname"></label>
    <label>Game ID: <input type="text" v-model="gid"></label>
    <button @click="joinGame">Join game</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      uname: '',
      gid: '',
    };
  },
  methods: {
    joinGame() {
      this.$socket.client.emit('join', {username:this.uname, game_id:this.gid});
    }
  },
  sockets: {
    join() {
      this.$router.push('/game');
    }
  }
}
</script>
