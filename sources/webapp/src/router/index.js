import Vue from 'vue'
import Router from 'vue-router'

import Index from '@/components/Index'
import Setup from '@/components/Setup'
import Config from '@/components/Config'
import NotFound from '@/components/NotFound'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
      props: true
    },
    {
      path: '/setup',
      name: 'Setup',
      component: Setup,
      props: true
    },
    {
      path: '/config',
      name: 'Config',
      component: Config,
      props: true
    },
    {
      path: '/404',
      name: '404',
      component: NotFound
    },
    {
      path: '*',
      redirect: '/404'
    }
  ]
})
