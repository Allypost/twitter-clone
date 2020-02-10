import { get, post } from "@/helpers/axios";
import Vue from "vue";

const TWEET_BASE = "/api/tweet";
const TIMELINE_BASE = `${ TWEET_BASE }/timeline`;

const fetchTimeline = async ({ type, page: rawPage }) => {
  const page = Math.max(1, Number(rawPage));

  switch (type) {
    case "public":
      return get(`${ TIMELINE_BASE }/public/${ Number(page) }`);
    case "my":
    case "mine":
      return get(`${ TIMELINE_BASE }/my/${ Number(page) }`);
    case "private":
      return get(`${ TIMELINE_BASE }/private/${ Number(page) }`);
    default:
      throw new Error("Unknown tweet type");
  }
};

const sortByCreatedAt =
        ({ created_at: a }, { created_at: b }) =>
          (new Date(b)) - (new Date(a))
;

const state = {
  tweets: [],
  metadata: {
    type: "my",
    page: 0,
    perPage: 0,
    total: 0,
    next: false,
    prev: false,
  },
};

const getters = {
  getTweets(state) {
    return state.tweets;
  },

  getMetadata(state) {
    return state.metadata;
  },
};

const mutations = {
  setTweets(state, tweets) {
    Vue.set(state, "tweets", [ ...tweets ].sort(sortByCreatedAt));
  },

  addTweet(state, tweet) {
    Vue.set(state, "tweets", [ ...state.tweets, tweet ].sort(sortByCreatedAt));
  },

  setMetadata(state, { type, page, perPage, total, next, prev }) {
    Vue.set(state, "metadata", { type, page, perPage, total, next, prev });
  },
};

const actions = {
  async tweet({ commit }, { text, imageId }) {
    const { success, errors, data } = await post(TWEET_BASE, { text, imageId });

    if (success) {
      commit("addTweet", data);
      return null;
    } else {
      return errors.join(" ");
    }
  },

  async fetchTimeline({ commit }, { page, type }) {
    const { success, data, errors } = await fetchTimeline({ type, page });

    if (success) {
      const { tweets, ...metadata } = data;

      commit("setTweets", tweets);
      commit("setMetadata", { ...metadata, type });

      return { errors, tweets, metadata };
    }

    return { errors, tweets: [], metadata: {} };
  },

  async fetchPublic({ dispatch }, { page }) {
    return dispatch("fetchTimeline", { page, type: "public" });
  },

  async fetchMy({ dispatch }, { page }) {
    return dispatch("fetchTimeline", { page, type: "my" });
  },

  async fetchPrivate({ dispatch }, { page }) {
    return dispatch("fetchTimeline", { page, type: "private" });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};