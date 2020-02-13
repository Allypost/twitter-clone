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
  {
    path: "/register",
    name: "Register",
  },
  {
    path: "/login",
    name: "Login",
  },
  {
    path: "/users",
    name: "Users",
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
        meta: {
          title: `Twitter Clone - ${ route.name }`,
          ...(route.meta || {}),
        },
        ...route,
      })),
});

router.beforeEach((to, from, next) => {
  const nearestWithTitle =
          to
            .matched
            .slice()
            .reverse()
            .find(
              (r) =>
                r.meta && r.meta.title,
            )
  ;

  if (nearestWithTitle) {
    document.title = nearestWithTitle.meta.title;
  }

  document
    .querySelectorAll("[data-vue-router-controlled]")
    .forEach(
      (el) =>
        el.parentNode.removeChild(el),
    )
  ;

  return next();
});

export default router;
