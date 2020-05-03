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
  created() {
    this.unwatch = this.$store.watch(
      state => state.gameState.started,
      newValue => {
        if (newValue) {
          console.log("Game started -- navigating to game view");
          this.$router.push("/game");
        }
      }
    )
  },
  beforeDestroy() {
    this.unwatch();
  }
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