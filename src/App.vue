<template>
  <div id="app">
    <InfoPanel></InfoPanel>
    <router-view></router-view>
  </div>
</template>

<script>
import InfoPanel from './components/InfoPanel.vue'

export default {
  name: 'App',
  components: {
    InfoPanel
  },
  mounted() {
    let playerID = localStorage.getItem('playerID');
    if (playerID) {
      this.$store.commit('setPlayerID', playerID);
    }
  }
}
</script>

<style>
body {
  background-color: #161f28;
  color: white;
}
table, th, td {
  border: 2px solid white;
  border-collapse: collapse;
  background-color: #2c3e50;
}
table {
  margin-left: auto;
  margin-right: auto;
  min-width: 20%;
}
td {
  text-align: left;
  padding: 5px 15px;
}
td:first-child {
  text-align: right;
  font-weight: bold;
}
a:link {
  color: #34c6eb;
}
a:visited{
  color: #be67e6;
}
nav {
  margin: 30px auto;
}
nav ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}
nav li {
  display: inline-block;
  margin: 0 5px;
}
nav a:link, nav a:visited {
  color: #34c6eb;
  background-color: #2c3e50;
  font-size: 20px;
  padding: 10px;
  border: 2px solid white;
  border-radius: 8px;
  font-weight: bold;
}
nav a:hover, nav a:active {
  color: #2c3e50;
  background-color: #34c6eb;
}
input {
  background-color: #2c3e50;
  border: 1px solid white;
  color: inherit;
}
button {
  color: #34c6eb;
  background-color: #2c3e50;
  font-size: 20px;
  padding: 10px;
  border: 2px solid white;
  border-radius: 8px;
  font-weight: bold;
  margin: 8px;
}
button:hover {
  color: #2c3e50;
  background-color: #34c6eb;
}
button:disabled {
  color: #bdbdbd;
  background-color: #2c3e50;
  font-size: 20px;
  padding: 10px;
  border: 2px solid #888888;
  border-radius: 8px;
  font-weight: bold;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 60px;
  max-width: 800px;
  margin: auto;
}
</style>
