<template>
  <div
    :style="{ backgroundImage: `url('${src}')` }"
  >
    <div :class="$style.actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<script>
  const fileReader = new FileReader();

  export default {
    name: "FilePreview",

    props: {
      file: {
        type: File,
        required: true,
      },
    },

    data: () => ({
      src: "",
    }),

    watch: {
      file() {
        this.refresh();
      },
    },

    mounted() {
      fileReader.onload =
        () =>
          this.$set(this, "src", fileReader.result)
      ;

      this.refresh();
    },

    methods: {

      refresh() {
        fileReader.readAsDataURL(this.file);
      },

    },
  };
</script>

<style lang="scss" module>
  .actions {
    position: absolute;
    top: .2em;
    right: .2em;
    display: flex;
    flex-direction: row-reverse;
  }
</style>
