import Vue from 'vue'
import Vuex from 'vuex'

import { getTaskStatus } from '@/api'

Vue.use(Vuex)

Vue.config.productionTip = false

function logStatus(store) {
  console.log('Task Status: ' + store.getters.taskStatus)
}

function logError(msg) {
  console.error('Error: ' + msg)
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
      store.pollInterval = setInterval(() => {
        getTaskStatus(payload.taskId)
          .then(response => {
            commit('setTaskId', payload.taskId)
            commit('setTaskStatus', response.data.status)
            commit('setTaskResults', response.data.pictures)  /* XXX FIXME BUG Change in API*/
          })
          .catch(err => {
            logError(err.message)
          })
        if (store.getters.taskStatus == 'COMPLETE' || store.getters.taskStatus == 'FAILED') {
          logStatus(store)
          clearInterval(store.pollInterval)
        }
      }, 250)
    }
  }
})

