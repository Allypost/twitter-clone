<template>
  <fieldset :class="$style.container">
    <legend>Timeline</legend>
    <section
      v-if="loading"
      :class="$style.loading"
    >
      <scale-loader
        :color="spinnerColor"
      />
    </section>
    <section
      :class="$style.timelineSelectContainer"
    >
      <label
        v-for="t in timelines"
        :key="t.type"
      >
        <input
          v-model="timeline"
          :class="$style.timelineSelect"
          :value="t.type"
          type="radio"
        >
        <span v-text="t.name" />
      </label>
    </section>

    <section
      v-if="tweets.length > 0"
    >
      <PaginationFooter
        v-model="page"
        :disabled="loading"
        :pagination-metadata="paginationMetadata"
      />
      <TimelineTweet
        v-for="tweet in tweets"
        :key="tweet.id"
        :tweet="tweet"
      />
      <PaginationFooter
        v-model="page"
        :disabled="loading"
        :pagination-metadata="paginationMetadata"
      />
    </section>
    <section
      v-else
    >
      <h2>Nothing Here...</h2>
      <h3>Yet.</h3>
    </section>
  </fieldset>
</template>

<script>
  import ScaleLoader from "vue-spinner/src/ScaleLoader";
  import { linkColorActive } from "@/assets/styles/_variables.scss";
  import PaginationFooter from "@/components/PaginationFooter";
  import TimelineTweet from "@/components/timeline/TimelineTweet";
  import { mapActions, mapGetters } from "vuex";

  export default {
    name: "TweetTimeline",

    components: { TimelineTweet, PaginationFooter, ScaleLoader },

    data: () => ({
      loading: true,
      timeline: "public",
      page: 1,
    }),

    computed: {

      timelines() {
        if (this.loggedIn) {
          return [
            { name: "Public", type: "public" },
            { name: "Following", type: "private" },
            { name: "My tweets", type: "my" },
          ];
        }

        return [];
      },

      spinnerColor() {
        return linkColorActive;
      },

      ...mapGetters({
        "tweets": "tweets/getTweets",
        "paginationMetadata": "tweets/getMetadata",
        "loggedIn": "user/loggedIn",
      }),

    },

    watch: {

      timeline() {
        if (1 !== this.page) {
          this.$set(this, "page", 1);
        } else {
          this.fetchTimeline();
        }
      },

      page() {
        this.fetchTimeline();
      },

    },

    created() {
      this.fetchTimeline();
    },

    methods: {
      async fetchTimeline() {
        this.$set(this, "loading", true);
        await this.doFetchTimeline({ type: this.timeline, page: this.page });
        this.$set(this, "loading", false);
      },

      ...mapActions({
        "doFetchTimeline": "tweets/fetchTimeline",
      }),
    },
  };
</script>

<style lang="scss" module>
  @import "../../assets/styles/global";

  .container {
    position: relative;
  }

  .loading {
    position: absolute;
    top: .9em;
    left: .3em;
  }

  .timeline-select-container {
    display: flex;
    align-items: center;
    justify-content: center;

    > label {
      margin: 0 .5em;
    }
  }

  .timeline-select {
    display: none;

    & + span {
      text-decoration: underline;
      text-decoration-style: dotted;

      &:hover {
        text-decoration-style: solid;
      }
    }

    &:checked + span {
      font-size: 110%;
      font-weight: bold;
    }
  }
</style>
