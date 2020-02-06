import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
  },
  {
    path: "/about",
    name: "About",
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes:
    [
      ...routes,
      // Add catch-all not found route at the end
      {
        path: "*",
        name: "Error/NotFound",
      },
    ]
      .map((route) => ({
        // Add (lazy-loaded) component to route if it doesn't have one set already
        component: () => import((`@/views/${ route.name }.vue`)),
        ...route,
      })),
});

export default router;
