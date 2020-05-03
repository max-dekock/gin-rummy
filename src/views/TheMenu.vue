<template>
  <div>
    <h1>Gin Rummy</h1>
    <nav>
      <ul>
        <li><router-link to="/create">New game</router-link></li>
        <li><router-link to="/join">Join game</router-link></li>
        <li><router-link to="/meldTest">Meld test</router-link></li>
      </ul>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  computed: {
    gameID() {
      return this.$store.state.gameID;
    },
    gameStarted() {
      return this.$store.state.gameState.started;
    }
  },
  watch: {
    gameID() {
      if (this.gameStarted) {
        this.$router.push('/game');
      }
    },
    gameStarted(newVal) {
      if (newVal) {
        this.$router.push('/game');
      }
    }
  },
}
</script>

<style scoped>
li {
  margin: 15px;
}
li * {
  display: inline-block;
  width: 150px;
}
</style>