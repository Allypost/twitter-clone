<template>
  <div class="home">
    <section
      v-if="loggedIn"
      :class="$style.section"
    >
      <CreateTweet
        style="font-size: 120%"
      />
    </section>
  </div>
</template>

<script>
  // @ is an alias to /src
  import CreateTweet from "@/components/timeline/CreateTweet";
  import { mapGetters } from "vuex";

  export default {
    name: "Home",

    components: {
      CreateTweet,
    },

    computed: {

      ...mapGetters({
        "loggedIn": "user/loggedIn",
      }),

    },

  };
</script>

<style lang="scss" module>
  .section {
    font-size: 130%;
    width: 40%;
    min-width: 500px;
    margin: 0 auto;
  }
</style>
