import Vue from 'vue'
import Vuex from 'vuex'

import { getTaskStatus } from '@/api'

Vue.use(Vuex)

Vue.config.productionTip = false

export const store = new Vuex.Store({
  state: {
    count: 0,
    task: {
        id: '',
        status: '',
        pictures: {}
    }
  },
  mutations: {
    increment (state) {
      state.count++
    },
    decrement (state) {
      state.count--
    }
  },
  actions: {
    async incrementAsync ({ commit }) {
      setTimeout(() => {
        commit('increment')
      }, 1000)
    },
    async decrementAsync ({ commit }) {
      setTimeout(() => {
        commit('decrement')
      }, 1000)
    },
    async getStatus({ taskId }) {
      getTaskStatus(taskId)
        .then(response => {
          this.state.task.status = response.data.status
        })
    }
  }
})
