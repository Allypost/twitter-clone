import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const requireAll =
        (r) =>
          Object.fromEntries(
            r
              .keys()
              .map(
                (mpath, ...args) => {
                  const result = r(mpath, ...args).default;
                  const name =
                          mpath
                            .replace(/(?:^[./]*\/|\.[^.]+$)/g, "") // Trim
                            .replace(/\//g, "_") // Relace '/'s by '_'s
                  ;

                  return [ name, result ];
                },
              ),
          );

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: requireAll(require.context("./modules", false, /\.js$/)),
});
