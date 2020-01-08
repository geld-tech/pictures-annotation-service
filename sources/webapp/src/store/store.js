import Vue from 'vue'
import Vuex from 'vuex'

import { getTaskStatus } from '@/api'

Vue.use(Vuex)

Vue.config.productionTip = false

export const store = new Vuex.Store({
  state: {
    task: {
        id: '',
        status: 'UNDEFINED',
        results: {}
    }
  },
  getters: {
    taskStatus: state => {
      return state.task.status
    }
  },
  mutations: {
    setTaskId(state, value) {
      state.task.id = value
    },
    setTaskStatus(state, value) {
      state.task.status = value
    },
    setTaskResults(state, value) {
      state.task.results = value
    }
  },
  actions: {
    async getStatus({ commit }, payload) {
      console.log('Starting '+store.getters.taskStatus)
      while (store.getters.taskStatus != 'COMPLETE' && store.getters.taskStatus != 'FAILED') {
        console.log('Looping '+store.getters.taskStatus)
        getTaskStatus(payload.taskId)
          .then(response => {
            console.log('RESPONSE XXX')
            console.log('RESPONSE '+response.data)
            commit('setTaskId', payload.taskId)
            commit('setTaskStatus', response.data.status)
            commit('setTaskResults', response.data.pictures)  /* XXX FIXME BUG Change in API*/
          })
          .catch(err => {
            console.log('ERROR '+err.message)
          })
        new Promise(resolve => setTimeout(resolve, 250))
      }
    }
  }
})
