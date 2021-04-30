import Vue from 'vue'
import Vuex from 'vuex'

// import example from './module-example'

Vue.use(Vuex)

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */
import general from 'src/store/general'
import account from 'src/store/account'
import session from 'src/store/session'

export default function (/* { ssrContext } */) {
  const Store = new Vuex.Store({
    modules: {
      general, account, session
    },

    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: process.env.DEBUGGING
  })

  return Store
}
