<template>
  <table>
    <tr>
      <td>Socket status</td>
      <td>{{ $socket.connected ? "Connected" : "Disconnected"}}</td>
    </tr>
    <tr>
      <td>Game ID</td>
      <td>{{ gameID }}</td>
    </tr>
    <tr>
      <td>Player ID</td>
      <td>{{ playerID }}</td>
    </tr>
    <tr>
      <td>Error message</td>
      <td>{{ error }}</td>
    </tr>
    <tr>
      <td>Emit</td>
      <td><a href="javascript:void(0)" @click="emitUpdate">update</a> <a href="javascript:void(0)" @click="emitRejoin">rejoin</a></td>
    </tr>
  </table>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['gameID', 'playerID', 'error'])
  },
  methods: {
    emitUpdate() {
      console.log('Emitting update');
      this.$socket.client.emit('update', {gameID: this.gameID});
    },
    emitRejoin() {
      console.log('Emitting rejoinGame');
      this.$socket.client.emit('rejoinGame', {gameID: this.gameID, playerID: this.playerID});
    }
  }
};
</script>
