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
    increment(state) {
      state.count++
    },
    decrement(state) {
      state.count--
    },
    setTaskId(state, value) {
      state.task.id = value
    },
    setTaskStatus(state, value) {
      state.task.status = value
    }
  },
  actions: {
    async incrementAsync({ commit }) {
      setTimeout(() => {
        commit('increment')
      }, 1000)
    },
    async decrementAsync({ commit }) {
      setTimeout(() => {
        commit('decrement')
      }, 1000)
    },
    async getStatus({ commit }, payload) {
      getTaskStatus(payload.taskId)
        .then(response => {
          commit('setStatus', response.data.status)
        })
    }
  }
})
