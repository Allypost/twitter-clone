<template>
  <article :class="$style.article">
    <div :class="$style.tweetImage" />
    <div :class="$style.tweetBody">
      <div :class="$style.tweetBodyHeader">
        <span :class="$style.tweetUser">{{ poster.username }}</span>
        <span :class="$style.separator">&#x22c5;</span>
        <abbr
          :class="$style.tweetDate"
          :title="date.toLocaleString()"
        >{{ formattedDate }}</abbr>
      </div>
      <blockquote
        :class="$style.tweetBodyText"
        v-text="tweet.text"
      />
    </div>
  </article>
</template>

<script>
  import { format } from "timeago.js";
  import { mapGetters } from "vuex";

  const requestIdleCallbackPolyfill = function(handler) {
    const startTime = Date.now();

    return (
      setTimeout(
        () => {
          handler({
            didTimeout: false,
            timeRemaining() {
              return Math.max(0, 50.0 - (Date.now() - startTime));
            },
          });
        },
        1,
      )
    );
  };

  const requestIdleCallback = window.requestIdleCallback || requestIdleCallbackPolyfill;

  export default {
    name: "TimelineTweet",

    props: {
      tweet: {
        type: Object,
        required: true,
      },
    },

    data() {
      return {
        formattedDate: "",
        dateListener: null,
      };
    },

    computed: {

      poster() {
        return this.tweet.poster;
      },

      date() {
        return new Date(this.tweet.created_at);
      },

      ...mapGetters({
        "loggedIn": "user/loggedIn",
      }),

    },

    mounted() {
      this.dateListener = setInterval(this.updateTimeAgo.bind(this), 1000);
      this.updateTimeAgo();
    },

    beforeDestroy() {
      clearInterval(this.dateListener);
    },

    methods: {

      updateTimeAgo() {
        const handler = () =>
          this.$set(this, "formattedDate", format(this.date))
        ;

        requestIdleCallback(handler);
      },

    },
  };
</script>

<style lang="scss" module>
  @import "../../assets/styles/variables";

  .article {
    display: flex;
    align-items: stretch;
    flex-basis: auto;
    flex-direction: row;
    flex-shrink: 0;
    box-sizing: border-box;
    margin-bottom: .5em;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .tweet-body {
    position: relative;
    display: flex;
    align-items: stretch;
    flex-direction: column;
    width: 100%;
    text-align: left;
  }

  .tweet-body-header {
    display: flex;
    align-items: center;
  }

  .tweet-user {
    font-weight: bold;
  }

  .separator {
    font-size: 85%;
    padding: 0 .25em;
    cursor: default;
    opacity: .7;
  }

  .tweet-date {
    font-size: 75%;
    font-weight: lighter;
    cursor: help;
  }

  .tweet-body-text {
    box-sizing: border-box;
    margin: .1em 0 .1em .4em;
    padding-left: .4em;
    white-space: pre-wrap;
    border-left: 1px solid #{$text-color};
  }
</style>
