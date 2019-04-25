// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import BootstrapVue from 'bootstrap-vue'
import { Alert, Collapse, Progress, Table, Navbar } from 'bootstrap-vue/es/components'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import { Bar, Line } from 'vue-chartjs'

Vue.use(BootstrapVue)
Vue.use(Alert)
Vue.use(Collapse)
Vue.use(Progress)
Vue.use(Table)
Vue.use(Navbar)

Vue.use(Bar)
Vue.use(Line)

Vue.config.productionTip = false

var vm = new Vue({
  el: '#app',
  router,
  render: h => h(App),
  components: { App },
  template: '<App/>'
})
vm.$mount('#main')
