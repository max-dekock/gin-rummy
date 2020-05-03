<template>
  <div>
    <span
      @click="toggle"
      style="color: lightgray; text-decoration: underline;"
    >
      {{ showPanel ? "Hide debug panel" : "Show debug panel" }}
    </span>
    <table v-if="showPanel">
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
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      showPanel: false,
    };
  },
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
    },
    toggle() {
      this.showPanel = !this.showPanel;
    }
  }
};
</script>
