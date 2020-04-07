import Vue from 'vue'

import App from './App.vue'

import VueSocketIOExt from 'vue-socket.io-extended'
import io from 'socket.io-client'

import store from './store'
import router from './routes'

const socket = io(`${window.location.host}`);
Vue.use(VueSocketIOExt, socket, {store});

Vue.config.productionTip = false

new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app')
