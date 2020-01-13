import Vue from 'vue'
import Vuex from 'vuex'

import { getTaskStatus } from '@/api'

Vue.use(Vuex)

Vue.config.productionTip = false

function logStatus(store) {
  console.log('Status '+store.getters.taskStatus)
}

export const store = new Vuex.Store({
  pollInterval: {},
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
      window.setInterval(() => {
        console.log('Checking '+store.getters.taskStatus)
        getTaskStatus(payload.taskId)
          .then(response => {
            console.log('RESPONSE XXX')
            console.log('RESPONSE '+response.data.status)
            commit('setTaskId', payload.taskId)
            commit('setTaskStatus', response.data.status)
            commit('setTaskResults', response.data.pictures)  /* XXX FIXME BUG Change in API*/
            console.log('RESPONSE OOO '+store.getters.taskStatus)
            logStatus(store)
          })
          .catch(err => {
            console.log('ERROR '+err.message)
          })
        console.log('Done '+store.getters.taskStatus)
      }
    }, 5000)
  }
})

