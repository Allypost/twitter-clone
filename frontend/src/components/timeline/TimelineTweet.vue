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
        <span :class="$style.editTools">
          <template
            v-if="loggedIn && poster.id !== currentUserId"
          >
            <button
              v-if="!isFollowingUser"
              :class="$style.followButton"
              :disabled="loading"
              @click.prevent="handleFollow(poster.id)"
            >
              Follow
            </button>
            <button
              v-else
              :class="$style.unfollowButton"
              :disabled="loading"
              @click.prevent="handleUnfollow(poster.id)"
            >
              Unfollow
            </button>
          </template>
          <template
            v-if="currentUserId === poster.id"
          >
            <button
              :class="$style.deleteButton"
              :disabled="loading"
              @click.prevent="handleDelete"
            >&#x1f5d1;</button>
          </template>
        </span>
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
  import { mapActions, mapGetters } from "vuex";

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

  const doAsync = (fn) => (async function(...args) {
    this.$set(this, "loading", true);
    const error = await fn.call(this, ...args);
    this.$set(this, "loading", false);

    if (error) {
      alert(error);
    }
  });

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
        loading: false,
      };
    },

    computed: {

      poster() {
        return this.tweet.poster;
      },

      date() {
        return new Date(this.tweet.created_at);
      },

      isFollowingUser() {
        return this.isFollowing(this.poster.id);
      },

      ...mapGetters({
        "loggedIn": "user/loggedIn",
        "currentUserId": "user/getId",
        "isFollowing": "user/isFollowing",
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

      async handleDelete() {
        const accepted = confirm("Are you sure you want to delete your tweet?");

        if (!accepted) {
          return;
        }

        await doAsync(
          async () =>
            await this.deleteTweet({ id: this.tweet.id }),
        );

        this.$set(this, "loading", true);
        const error = await this.deleteTweet({ id: this.tweet.id });
        this.$set(this, "loading", false);

        if (error) {
          alert(error);
        }
      },

      handleFollow: doAsync(
        async function(userId) {
          return await this.followUser({ id: userId });
        },
      ),

      handleUnfollow: doAsync(
        async function(userId) {
          return this.unfollowUser({ id: userId });
        },
      ),

      updateTimeAgo() {
        const handler = () =>
          this.$set(this, "formattedDate", format(this.date))
        ;

        requestIdleCallback(handler);
      },

      ...mapActions({
        "deleteTweet": "tweets/deleteTweet",
        "followUser": "user/follow",
        "unfollowUser": "user/unfollow",
      }),

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
  }

  .tweet-body-text {
    box-sizing: border-box;
    margin: .1em 0 .1em .4em;
    padding-left: .4em;
    white-space: pre-wrap;
    border-left: 1px solid #{$text-color};
  }

  .edit-tools {
    margin-left: auto;
  }

  %tools-button-base {
    font-size: 75%;
    margin-right: 10px;
    padding: .2em .3em;
    color: $text-color;
    border: 2px solid #{$text-color};
    border-radius: 4px;
    background-color: transparentize($link-color-active, .95);

    &:last-child {
      margin-right: inherit;
    }

    &:hover {
      background-color: transparentize($link-color-active, .9);
    }
  }

  .follow-button {
    @extend %tools-button-base;
  }

  .unfollow-button {
    @extend %tools-button-base;

    border-color: complement($link-color-active);
    background-color: transparentize(complement($link-color-active), .95);

    &:hover {
      background-color: transparentize(complement($link-color-active), .9);
    }
  }

  .delete-button {
    @extend %tools-button-base;

    $color: #e53935;

    border-color: $color;
    background-color: transparentize($color, .95);

    &:hover {
      background-color: transparentize($color, .9);
    }
  }
</style>
