<template>
  <form
    action="/api/tweet"
    method="post"
    @submit.prevent="handleSubmit"
  >
    <fieldset>
      <legend>Tweet</legend>
      <p :class="$style.tweetContainer">
        <label>
          <textarea-autosize
            v-model="inputs.text"
            :class="$style.textarea"
            :disabled="posting"
            :max-height="350"
            placeholder="Type something here..."
            @keydown.native="handleKeydown"
          />
        </label>
      </p>
      <div :class="$style.submitContainer">
        <span :class="$style.spacer" />
        <scale-loader
          v-if="posting"
          :color="spinnerColor"
          height="1em"
        />
        <span :class="$style.textInfo">
          <radial-progress-bar
            :animate-speed="100"
            :completed-steps="Math.min(inputs.text.length, maxLength)"
            :diameter="circleDiameter"
            :start-color="circleFillColour"
            :stop-color="circleFillColour"
            :stroke-width="2"
            :total-steps="maxLength"
            :class="$style.textProgress"
            inner-stroke-color="#e0e0e0"
          >
            <template v-if="textTooLong">
              {{ inputs.text.length - maxLength }}
            </template>
          </radial-progress-bar>
        </span>
        <input
          :disabled="textTooLong || posting"
          :class="$style.tweetButton"
          type="submit"
          value="Tweet"
        >
      </div>
    </fieldset>
  </form>
</template>

<script>
  import RadialProgressBar from "vue-radial-progress";
  import { mapActions } from "vuex";
  import ScaleLoader from "vue-spinner/src/ScaleLoader";
  import { linkColorActive } from "@/assets/styles/_variables.scss";

  export default {
    name: "CreateTweet",

    components: { RadialProgressBar, ScaleLoader },

    data: () => ({
      inputs: {
        text: "",
        imageId: null,
      },
      maxLength: 140,
      posting: false,
      submitError: "",
    }),

    computed: {

      textTooLong() {
        const { inputs: { text }, maxLength } = this;
        return text.length > maxLength;
      },

      textNotTooLong() {
        return !this.textTooLong;
      },

      circleFillColour() {
        if (this.textNotTooLong) {
          return "#00bcd4";
        }

        return "#d32f2f";
      },

      circleDiameter() {
        if (this.textNotTooLong) {
          return 25;
        }

        return 35;
      },

      spinnerColor() {
        return linkColorActive;
      },

    },

    methods: {

      async handleKeydown(e) {
        if (e.ctrlKey && 13 === e.keyCode) {
          e.preventDefault();

          await this.handleSubmit();
        }
      },

      async handleSubmit() {
        this.$set(this, "submitError", "");

        this.$set(this, "posting", true);
        const error = await this.tweet(this.inputs);
        this.$set(this, "posting", false);

        if (error) {
          this.$set(this, "submitError", error);
        } else {
          this.$set(this.inputs, "text", "");
          this.$set(this.inputs, "imageId", null);
        }
      },

      ...mapActions({
        "tweet": "tweets/tweet",
      }),

    },
  };
</script>

<style lang="scss" module>
  @import "../../assets/styles/variables";

  .textarea {
    $padding: .6em;

    font-size: 110%;
    width: 100%;
    padding: #{$padding / 2} #{$padding};
  }

  .tweet-container {
    margin: .1em 0;
  }

  .submit-container {
    display: flex;
    align-items: center;
    text-align: right;

    & > * {
      margin-right: 10px;

      &:last-child {
        margin-right: initial;
      }
    }
  }

  .spacer {
    margin-left: auto;
  }

  .text-info {
    font-size: 16px;
    text-align: right;
    opacity: .7;
    color: #e53935;

    .text-progress {
      display: inline-block;
      transition-timing-function: ease-in-out;
      transition-duration: 300ms;
      transition-property: width, height;
    }
  }
</style>
