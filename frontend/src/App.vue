<template>
  <main>
    <nav :id="$style.nav">
      <router-link :to="{ name: 'Home' }">
        Home
      </router-link>
      |
      <router-link :to="{ name: 'Users' }">
        Users
      </router-link>
      <template v-if="loggedIn">
        |
        <a href="#">{{ currentUserUsername }}</a>
        |
        <a
          href="/logout"
          @click.prevent="logout"
        >Logout</a>
      </template>
      <template v-else>
        |
        <router-link :to="{ name: 'Login' }">
          Login
        </router-link>
        |
        <router-link :to="{ name: 'Register' }">
          Register
        </router-link>
      </template>
    </nav>
    <main>
      <router-view />
    </main>
  </main>
</template>

<script>
  import { mapActions, mapGetters } from "vuex";

  export default {
    computed: {
      ...mapGetters({
        "loggedIn": "user/loggedIn",
        "currentUserUsername": "user/getUsername",
      }),
    },

    created() {
      window.$store = this.$store;
      this.fetchUser();
    },

    methods: {
      ...mapActions({
        "fetchUser": "user/fetchAll",
        "logout": "user/logout",
      }),
    },
  };
</script>

<style lang="scss" src="./assets/styles/global.scss"></style>
<style lang="scss" module>
  #nav {
    font-size: 150%;
    padding: 30px;
  }
</style>
