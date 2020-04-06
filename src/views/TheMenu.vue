<template>
  <div id="app">
    <h1>Gin Rummy</h1>
    <nav>
      <ul>
        <li><router-link to="/create">Create new game</router-link></li>
        <li><router-link to="/join">Join game</router-link></li>
        <li><router-link to="/meldTest">Meld test</router-link></li>
        <li><router-link to="/knockTest">Knock test</router-link></li>
      </ul>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  created() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters.gameStarted,
      (newValue) => {
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