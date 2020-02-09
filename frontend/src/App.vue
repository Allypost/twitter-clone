<template>
  <div id="app">
    <nav id="nav">
      <router-link :to="{ name: 'Home' }">Home</router-link>
      |
      <router-link :to="{ name: 'About' }">About</router-link>
      <template v-if="loggedIn">
        |
        <a @click.prevent="logout" href="/logout">Logout</a>
      </template>
      <template v-else>
        |
        <router-link :to="{ name: 'Login' }">Login</router-link>
        |
        <router-link :to="{ name: 'Register' }">Register</router-link>
      </template>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
  import { mapActions, mapGetters } from "vuex";

  export default {
    created() {
      window.$store = this.$store;
      this.fetchUser();
    },

    computed: {
      ...mapGetters({
        "loggedIn": "user/loggedIn",
      }),
    },

    methods: {
      ...mapActions({
        "fetchUser": "user/fetchUser",
        "logout": "user/logout",
      }),
    },
  };
</script>

<style lang="scss" src="./assets/styles/global.scss"></style>
<style lang="scss" scoped>
  #nav {
    padding: 30px;
  }
</style>
