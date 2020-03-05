import Vue from 'vue'
import store from './store';
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueSocketIO from 'vue-socket.io'

Vue.use(new VueSocketIO({
  debug: false,
  connection: 'http://localhost:5000',
}))

Vue.config.productionTip = false

new Vue({
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
