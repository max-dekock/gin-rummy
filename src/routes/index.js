import Vue from 'vue'
import Router from 'vue-router'
import TheMenu from '../views/TheMenu.vue'
import TheMenuNewGame from '../views/TheMenuNewGame.vue'
import TheMenuJoinGame from '../views/TheMenuJoinGame.vue'
import GameInterface from '../views/GameInterface.vue'
import MeldTest from '../views/MeldTest.vue'
import KnockTest from '../views/KnockTest.vue'

Vue.use(Router);

export default new Router({
  routes: [
    { path: '/', component: TheMenu,
        children: [
          { path: 'create', component: TheMenuNewGame},
          { path: 'join', component: TheMenuJoinGame},
          { path: 'meldTest', component: MeldTest},
          { path: 'knockTest', component: KnockTest},
        ]
    },
    { path: '/game', component: GameInterface}
  ]
});
