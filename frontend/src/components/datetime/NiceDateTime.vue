<template>
  <Datetime
    v-bind="{
      ...$attrs,
      phrases,
      value,
      maxDatetime,
      type: 'datetime',
      auto: true
    }"
    @input="$emit('input', $event)"
  />
</template>

<script>
  import { Datetime } from "vue-datetime";

  export default {
    name: "NiceDateTime",

    components: { Datetime },

    inheritAttrs: false,

    props: {
      value: {
        type: [ String, Date ],
        required: true,
      },
    },

    computed: {
      now() {
        return (new Date()).toISOString();
      },

      phrases() {
        return {
          ok: "Continue",
          cancel: "Exit",
        };
      },

      maxDatetime() {
        return this.$attrs.maxDatetime || this.now;
      },
    },
  };
</script>

<style src="vue-datetime/dist/vue-datetime.css" />
