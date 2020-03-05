import Vue from 'vue'
import store, {base} from './store';
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueSocketIO from 'vue-socket.io'

Vue.use(new VueSocketIO({
  debug: false,
  connection: base,
}))

Vue.config.productionTip = false

new Vue({
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
