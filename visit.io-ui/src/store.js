import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    city: null
  },
  mutations: {
    setCity (state, city) {
      state.city = city
    }
  },
  actions: {
    updateCity: (context, payload) => {
      context.commit('setCity', payload)
    }
  },
  getters: {
    city: state => state.city
  }
})
