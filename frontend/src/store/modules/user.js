import { get, post } from "@/helpers/axios";
import Vue from "vue";

const AUTH_BASE = "/api/auth";
const USER_BASE = "/api/user";

const sessionSetter = (name) => ((value) => {
  sessionStorage.setItem(name, JSON.stringify(value));
});

const sessionGetter = (name, url) => (async (force = false) => {
  const localData = JSON.parse(sessionStorage.getItem(name));

  if (localData && !force) {
    return localData;
  }

  const { data = null } = await get(url);

  return data;
});

const getUser = sessionGetter("user", `${ USER_BASE }/me`);
const getFollowers = sessionGetter("followers", `${ USER_BASE }/followers`);
const getFollowing = sessionGetter("following", `${ USER_BASE }/following`);

const setUser = sessionSetter("user");
const setFollowers = sessionSetter("followers");
const setFollowing = sessionSetter("following");

/**
 * Mostly used for converting arrays to something with an O(1) lookup
 */
const arrayToObject = (array) => Object.fromEntries(array.map((x) => [ x, x ]));

const state = {
  user: null,
  followers: {},
  following: {},
};

const getters = {

  loggedIn({ user }) {
    return null !== user;
  },

  getUsername({ user }) {
    return user ? String(user.username) : "";
  },

  getId({ user }) {
    return Number(user && user.id);
  },

  getFollowing({ following }) {
    return following;
  },

  getFollowers({ followers }) {
    return followers;
  },

  isFollowing: ({ following }) => (id) => id in following,

};

const mutations = {

  setUser(state, user) {
    Vue.set(state, "user", user);
    setUser(user);
  },

  setFollowing(state, following) {
    const followingObject =
            Array.isArray(following)
            ? arrayToObject(following)
            : following
    ;

    Vue.set(state, "following", followingObject);
    setFollowing(followingObject);
  },

  setFollowers(state, followers) {
    const followersObject =
            Array.isArray(followers)
            ? arrayToObject(followers)
            : followers
    ;

    Vue.set(state, "followers", followersObject);
    setFollowers(followersObject);
  },

};

const actions = {

  async logout({ commit }) {
    await post(`${ AUTH_BASE }/logout`);

    commit("setUser", null);
  },

  async fetchAll({ dispatch }, { force = false } = {}) {
    await dispatch("fetchUser", force);
    await dispatch("fetchFollowers", force);
    await dispatch("fetchFollowing", force);
  },

  async fetchUser({ commit }, { force = false } = {}) {
    const data = await getUser(force);

    commit("setUser", data);
  },

  async fetchFollowers({ commit }, { force = false } = {}) {
    const data = await getFollowers(force);

    commit("setFollowers", data);
  },

  async fetchFollowing({ commit }, { force = false } = {}) {
    const data = await getFollowing(force);

    commit("setFollowing", data);
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

  async follow({ commit }, { id }) {
    const { success, errors, data } = await post(`${ USER_BASE }/follow`, { id });

    if (success) {
      commit("setFollowing", data);
      return null;
    } else {
      return errors.join(" ");
    }
  },

  async unfollow({ commit }, { id }) {
    const { success, errors, data } = await post(`${ USER_BASE }/unfollow`, { id });

    if (success) {
      commit("setFollowing", data);
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
