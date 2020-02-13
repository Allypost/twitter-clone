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
    <main :class="$style.container">
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

  .container {
    width: 50%;
    margin: 0 auto;
    transition: width 300ms ease-out;

    @media screen and (min-width: 1668px) {
      width: 40%;
    }

    @media screen and (max-width: 1172px) {
      width: 65%;
    }

    @media screen and (max-width: 776px) {
      width: 85%;
    }

    @media screen and (max-width: 564px) {
      width: 95%;
    }
  }
</style>
