import Vue from 'vue'
import Vuex from 'vuex'

import { getTaskStatus } from '@/api'

Vue.use(Vuex)

Vue.config.productionTip = false

export const store = new Vuex.Store({
  state: {
    task: {
        id: '',
        status: '',
        results: {}
    }
  },
  getters: {
    getTaskStatus: state => {
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
      while (true) {
        getTaskStatus(payload.taskId)
          .then(response => {
            commit('setTaskId', payload.taskId)
            commit('setTaskStatus', response.data.status)
            commit('setTaskResults', response.data.pictures)  /* XXX FIXME BUG Change in API*/
          })
        if (state.task.status != 'PENDING') {            
          break;
        } 
        new Promise(resolve => setTimeout(resolve, 250));
      }
    }
  }
})
