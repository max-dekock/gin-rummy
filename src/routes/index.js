import Vue from 'vue'
import Router from 'vue-router'
import TheMenu from '../views/TheMenu.vue'
import TheMenuNewGame from '../views/TheMenuNewGame.vue'
import TheMenuJoinGame from '../views/TheMenuJoinGame.vue'
import GameInterface from '../views/GameInterface2.vue'
import MeldTest from '../views/MeldTest.vue'

Vue.use(Router);

export default new Router({
  routes: [
    { path: '/', component: TheMenu,
        children: [
          { path: 'create', component: TheMenuNewGame },
          { path: 'join', component: TheMenuJoinGame },
        ]
    },
    { path: '/game', component: GameInterface },
    { path: '/meldTest', component: MeldTest }
  ]
});
