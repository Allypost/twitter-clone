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
    <section :class="$style.section">
      <TweetTimeline />
    </section>
  </div>
</template>

<script>
  // @ is an alias to /src
  import CreateTweet from "@/components/timeline/CreateTweet";
  import TweetTimeline from "@/components/timeline/TweetTimeline";
  import { mapGetters } from "vuex";

  export default {
    name: "Home",

    components: {
      CreateTweet,
      TweetTimeline,
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
    width: 100%;
  }
</style>
