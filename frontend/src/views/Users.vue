<template>
  <section :class="$style.container">
    <section>
      <fieldset>
        <legend>Search</legend>

        <p>
          <label>
            Username:
            <input
              v-model="query"
              type="text"
            >
          </label>
        </p>

        <h3 v-if="error">
          {{ error }}
        </h3>
      </fieldset>
    </section>

    <section>
      <fieldset :class="$style.usersContainer">
        <legend>Users</legend>

        <section
          v-if="loading"
          :class="$style.loading"
        >
          <scale-loader
            :color="spinnerColor"
          />
        </section>

        <section
          v-if="users.length"
        >
          <PaginationFooter
            v-model="page"
            :pagination-metadata="metadata"
          />

          <section :class="$style.userList">
            <div
              v-for="(user, i) in users"
              :key="user.id"
              :class="[ $style.userEntry, i % 2 === 0 ? $style.userEntryEven : $style.userEntryOdd ]"
            >
              <strong>{{ user.username }}</strong>
              <span :class="$style.separator">&#x22c5;</span>
              <span>
                joined
                <abbr
                  :class="$style.tweetDate"
                  :title="user.created_at | dateToLocale"
                >{{ user.created_at | timeAgo }}</abbr>
              </span>
              <span style="margin-left: auto;" />
              <template
                v-if="loggedIn && user.id !== currentUserId"
              >
                <button
                  v-if="!isFollowing(user.id)"
                  :class="$style.followButton"
                  :disabled="loading !== 0"
                  @click.prevent="handleFollow(user.id)"
                >
                  Follow
                </button>
                <button
                  v-else
                  :class="$style.unfollowButton"
                  :disabled="loading !== 0"
                  @click.prevent="handleUnfollow(user.id)"
                >
                  Unfollow
                </button>
              </template>
            </div>
          </section>

          <PaginationFooter
            v-model="page"
            :pagination-metadata="metadata"
          />
        </section>
        <template
          v-else
        >
          <h2>Nothing found</h2>
        </template>
      </fieldset>
    </section>
  </section>
</template>

<script>
  import { format } from "timeago.js";
  import { throttle } from "lodash";
  import { mapActions, mapGetters } from "vuex";
  import ScaleLoader from "vue-spinner/src/ScaleLoader";
  import PaginationFooter from "@/components/PaginationFooter";
  import { linkColorActive } from "@/assets/styles/_variables.scss";

  const doAsync = (fn) => (async function(...args) {
    ++this.loading;
    const error = await fn.call(this, ...args);
    --this.loading;

    this.$set(this, "error", error);
  });

  export default {
    name: "Users",

    components: { PaginationFooter, ScaleLoader },

    filters: {

      dateToLocale(value) {
        return (new Date(value)).toLocaleString();
      },

      timeAgo(date) {
        return format(new Date(date));
      },

    },

    data: () => ({
      users: [],
      metadata: {},
      query: "",
      page: 1,
      error: "",
      loading: 0,
    }),

    computed: {

      boundPage() {
        return Math.min(this.page, this.metadata.total || 1);
      },

      spinnerColor() {
        return linkColorActive;
      },

      ...mapGetters({
        "loggedIn": "user/loggedIn",
        "currentUserId": "user/getId",
        "isFollowing": "user/isFollowing",
      }),

    },

    watch: {
      query() {
        this.debouncedSearch();
      },

      page() {
        this.search();
      },

      "metadata.total"() {
        if (this.boundPage < this.page) {
          this.$set(this, "page", this.boundPage);
        }
      },
    },

    mounted() {
      this.search();
    },

    methods: {

      debouncedSearch: throttle(function() {
        return this.search();
      }, 500),

      async search() {
        this.$set(this, "error", "");

        ++this.loading;
        const { success, errors, data } = await this.doSearch({ query: this.query, page: this.page });
        --this.loading;

        if (!success) {
          this.$set(this, "error", errors.join(" "));
          return null;
        }

        const { items, ...metadata } = data;

        this.$set(this, "users", items);
        this.$set(this, "metadata", metadata);
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

      ...mapActions({
        "doSearch": "user/search",
        "followUser": "user/follow",
        "unfollowUser": "user/unfollow",
      }),

    },
  };
</script>

<style lang="scss" module>
  @import "../assets/styles/variables";

  .container {
    width: 40%;
    margin: 0 auto;
  }

  .users-container {
    position: relative;
  }

  .loading {
    position: absolute;
    top: .9em;
    left: .3em;
  }

  .user-list {
    display: flex;
    flex-direction: column;
  }

  .user-entry {
    font-size: 120%;
    display: flex;
    align-items: center;
    padding: .2em .4em;

    &-even {
    }

    &-odd {
      background-color: transparentize(invert($background-color), .95);
    }
  }

  .separator {
    font-size: 85%;
    padding: 0 .25em;
    cursor: default;
    opacity: .7;
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
</style>
