import { get, post, request } from "@/helpers/axios";
import axios from "axios";
import Vue from "vue";
import VueTextareaAutosize from "vue-textarea-autosize";
import App from "./App.vue";
import router from "./router";
import store from "./store";

Vue.use(VueTextareaAutosize);

Vue.config.productionTip = false;

Vue.prototype.$http = axios;
Vue.prototype.$request = request;
Vue.prototype.$get = get;
Vue.prototype.$post = post;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
