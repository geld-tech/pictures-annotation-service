import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

Vue.config.productionTip = false

export const store = new Vuex.Store({
  state: {
    count: 0
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
    incrementAsync ({ commit }) {
      setTimeout(() => {
        commit('increment')
      }, 1000)
    },
    decrementAsync ({ commit }) {
      setTimeout(() => {
        commit('decrement')
      }, 1000)
    }
  }
})
