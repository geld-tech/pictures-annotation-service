// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

import App from './App'
import router from './router'

import BootstrapVue from 'bootstrap-vue'
import Alert from 'bootstrap-vue'
import Collapse from 'bootstrap-vue'
import Navbar from 'bootstrap-vue'
import Progress from 'bootstrap-vue'
import Table from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(Alert)
Vue.use(Collapse)
Vue.use(Navbar)
Vue.use(Progress)
Vue.use(Table)

Vue.config.productionTip = false

import { store } from './store/store'

var vm = new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App),
  components: { App },
  template: '<App/>'
})
vm.$mount('#main')
