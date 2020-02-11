import Vue from "vue";
import Vuex from "vuex";
import createMutationsSharer from "vuex-shared-mutations";

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
  plugins: [
    createMutationsSharer({
      predicate: (mutation) => mutation.type.startsWith("user/"),
    }),
  ],
});
