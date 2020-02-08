import { get, post } from "@/helpers/axios";
import Vue from "vue";

const getUser = async () => {
  const localUser = JSON.parse(sessionStorage.getItem("user"));

  if (localUser) {
    return localUser;
  }

  const { data = null } = await get("/api/auth/me");

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

};

const mutations = {

  setUser(state, user) {
    Vue.set(state, "user", user);
    setUser(user);
  },

};

const actions = {

  async logout({ commit }) {
    await post("/api/auth/logout");

    commit("setUser", null);
  },

  async fetchUser({ commit }) {
    const data = await getUser();

    commit("setUser", data);
  },

};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
