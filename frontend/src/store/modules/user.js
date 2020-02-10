import { get, post } from "@/helpers/axios";
import Vue from "vue";

const AUTH_BASE = "/api/auth";

const getUser = async () => {
  const localUser = JSON.parse(sessionStorage.getItem("user"));

  if (localUser) {
    return localUser;
  }

  const { data = null } = await get(`${ AUTH_BASE }/me`);

  return data;
};

const setUser = (user) => {
  sessionStorage.setItem("user", JSON.stringify(user));
};

const state = {
  user: null,
};

const getters = {

  loggedIn({ user }) {
    return null !== user;
  },

  getId({ user }) {
    return Number(user && user.id);
  },

};

const mutations = {

  setUser(state, user) {
    Vue.set(state, "user", user);
    setUser(user);
  },

};

const actions = {

  async logout({ commit }) {
    await post(`${ AUTH_BASE }/logout`);

    commit("setUser", null);
  },

  async fetchUser({ commit }) {
    const data = await getUser();

    commit("setUser", data);
  },

  async login({ commit }, { username, password }) {
    const { success, errors, data } = await post(`${ AUTH_BASE }/login`, { username, password });

    if (success) {
      commit("setUser", data);
      return null;
    } else {
      return errors.join(" ");
    }
  },

  async register({ commit }, { username, password, passwordRepeat }) {
    const { success, errors, data } = await post(`${ AUTH_BASE }/register`, { username, password, passwordRepeat });

    if (success) {
      commit("setUser", data);
      return null;
    } else {
      return errors.join(" ");
    }
  },

};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
