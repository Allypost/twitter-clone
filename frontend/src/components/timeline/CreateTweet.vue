<template>
  <form
    action="/api/tweet"
    method="post"
    @submit.prevent="handleSubmit"
  >
    <fieldset>
      <legend>Tweet</legend>

      <div
        :class="{ [$style.tweetContainer]: true, [$style.tweetDragover]: preview.hovering }"
        @dragleave="preview.hovering=false"
        @dragover.prevent="preview.hovering=true"
        @drop.prevent="handleDrop"
      >
        <file-preview
          v-if="preview.file"
          :class="$style.imagePreview"
          :file="preview.file"
        >
          <template
            v-slot:actions
          >
            <span
              :class="$style.imagePreviewClearButton"
              @click.prevent="handleClearPreview"
            >
              <x-icon size="1x" />
            </span>
          </template>
        </file-preview>

        <textarea-autosize
          ref="textInput"
          v-model="inputs.text"
          :class="$style.textarea"
          :disabled="posting"
          :max-height="350"
          placeholder="Type something here..."
          @keydown.native="handleKeydown"
        />
      </div>
      <progress
        v-if="uploading"
        :class="$style.uploadProgress"
        :max="upload.total"
        :value="upload.current"
      />
      <div :class="$style.submitContainer">
        <span
          v-if="submitError"
          :class="$style.submitError"
          v-text="submitError"
        />

        <span :class="$style.spacer" />

        <scale-loader
          v-if="posting"
          :color="spinnerColor"
          height="1em"
        />

        <span :class="$style.textInfo">
          <radial-progress-bar
            :animate-speed="100"
            :class="$style.textProgress"
            :completed-steps="Math.min(inputs.text.length, maxLength)"
            :diameter="circleDiameter"
            :start-color="circleFillColour"
            :stop-color="circleFillColour"
            :stroke-width="2"
            :total-steps="maxLength"
            inner-stroke-color="#e0e0e0"
          >
            <template v-if="textTooLong">
              {{ inputs.text.length - maxLength }}
            </template>
          </radial-progress-bar>
        </span>

        <label :class="$style.fileInputContainer">
          <span
            :class="$style.fileUploadButton"
            title="Upload image"
          >
            <image-icon />
          </span>
          <input
            ref="imageInput"
            accept="image/jpeg, image/gif"
            style="display: none"
            type="file"
            @change="updateFile($event.target.files[0])"
          >
        </label>

        <input
          :disabled="textTooShort || textTooLong || posting"
          type="submit"
          value="Tweet"
        >
      </div>
    </fieldset>
  </form>
</template>

<script>
  import FilePreview from "@/components/tweet/FilePreview";
  import RadialProgressBar from "vue-radial-progress";
  import { mapActions } from "vuex";
  import ImageIcon from "vue-feather-icons/icons/ImageIcon";
  import XIcon from "vue-feather-icons/icons/XIcon";
  import ScaleLoader from "vue-spinner/src/ScaleLoader";
  import { linkColorActive } from "@/assets/styles/_variables.scss";

  export default {
    name: "CreateTweet",

    components: { FilePreview, RadialProgressBar, ScaleLoader, XIcon, ImageIcon },

    data: () => ({
      inputs: {
        text: "",
        imageId: null,
      },
      preview: {
        hovering: false,
        file: null,
      },
      upload: {
        current: 23,
        total: 60,
      },
      maxLength: 140,
      submitting: false,
      uploading: false,
      submitError: "",
    }),

    computed: {

      posting() {
        return this.submitting || this.uploading;
      },

      imageAccepts() {
        const { accept } = this.$refs.imageInput;
        return Object.fromEntries(
          accept
            .split(",")
            .map((s) => s.toLowerCase().trim())
            .map((s) => [ s, s ]),
        );
      },

      textTooShort() {
        const { inputs: { text } } = this;

        return 1 >= text.length;
      },

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

      async handleDrop(ev) {
        this.$set(this.preview, "hovering", false);

        if (this.posting) {
          return;
        }

        const file = (() => {
          if (ev.dataTransfer.files) {
            return ev.dataTransfer.files[ 0 ];
          }

          const file = Array
            .from(ev.dataTransfer.items)
            .find(({ kind }) => "file" === kind)
          ;

          if (!file) {
            return null;
          }

          return file.getAsFile();
        })();

        if (!file) {
          return;
        }

        await this.updateFile(file);
      },

      async handleClearPreview() {
        this.$set(this.preview, "file", null);
      },

      async updateFile(file) {
        this.$set(this, "submitError", "");

        if (!(file.type in this.imageAccepts)) {
          this.$set(this, "submitError", "Image must be a .png or .jpeg");
          return;
        }

        this.$set(this.preview, "file", file);
        await this.$refs.textInput.$el.focus();
      },

      async handleKeydown(e) {
        if (e.ctrlKey && 13 === e.keyCode) {
          e.preventDefault();

          await this.handleSubmit();
        }
      },

      async handleSubmit() {
        this.$set(this, "submitError", "");

        const fileSuccess = await this.handleUpload();

        if (!fileSuccess) {
          return;
        }

        this.$set(this, "submitting", true);
        const error = await this.tweet(this.inputs);
        this.$set(this, "submitting", false);

        if (error) {
          this.$set(this, "submitError", error);
        } else {
          this.$set(this.inputs, "text", "");
          this.$set(this.inputs, "imageId", null);
          this.$set(this.preview, "file", null);
        }
      },

      async handleUpload() {
        if (!this.preview.file) {
          return true;
        }

        this.$set(this, "uploading", true);
        const { error, data } = await this.uploadFile({
          file: this.preview.file,
          /** @param {ProgressEvent} progress */
          onProgress: (progress) => {
            const { loaded, total } = progress;

            this.$set(this.upload, "current", loaded);
            this.$set(this.upload, "total", total);
          },
        });
        this.$set(this, "uploading", false);

        if (error) {
          this.$set(this, "submitError", error);
          return false;
        } else {
          this.$set(this.inputs, "imageId", data.id);
          return true;
        }
      },

      ...mapActions({
        "tweet": "tweets/tweet",
        "uploadFile": "file/upload",
      }),

    },
  };
</script>

<style lang="scss" module>
  @import "../../assets/styles/variables";

  .textarea {
    $padding: .6em;

    font-size: 110%;
    order: 1;
    width: 100%;
    padding: #{$padding / 2} #{$padding};
  }

  .image-preview {
    position: relative;
    display: block;
    order: 2;
    box-sizing: border-box;
    width: 100%;
    height: 300px;
    border: 1px solid invert($background-color);
    border-top: none !important;
    border-bottom-right-radius: 4px;
    border-bottom-left-radius: 4px;
    background-color: $background-color;
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
  }

  .image-preview + .textarea {
    border-bottom-style: dashed;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
  }

  .image-preview-clear-button {
    display: inline-block;
    width: 1.3em;
    height: 1.3em;
    padding: .15em;
    cursor: pointer;
    border-radius: 100%;
    background-color: rgba(0, 0, 0, .75);

    &:hover {
      background-color: rgba(0, 0, 0, .9);
    }

    > svg {
      width: 100%;
      height: 100%;
      color: #fafafa;
      fill: currentcolor;
    }
  }

  .upload-progress {
    width: 100%;
  }

  .tweet-container {
    line-height: 0;
    display: flex;
    flex-direction: column;
  }

  .tweet-container, .submit-container, .upload-progress {
    margin: .1em 0;
  }

  .tweet-dragover {
    > * {
      border-style: dashed;
      border-color: $link-color-active;
    }
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

  .submit-error {
    font-size: initial;
    padding-left: 2px;
    color: #e53935;
  }

  .spacer {
    margin-left: auto;
  }

  .text-info {
    font-size: 16px;
    display: inline-flex;
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

  .file-input-container {
    display: inline-flex;
    align-items: center;
  }

  .file-upload-button {
    display: inline-flex;
    min-width: 1.3em;
    color: $link-color;

    &:hover {
      color: $link-color-active;
    }

    > svg {
      width: 100%;
      height: 100%;
    }
  }
</style>
