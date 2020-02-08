<template>
  <p>
    <label :for="id">
      <span v-if="label">
        {{ label }}:
        <abbr
          title="Required"
          v-if="required"
        >*</abbr>
      </span>
    </label>
    <input
      :disabled="disabled"
      :id="id"
      :name="name"
      :required="required"
      :type="type"
      :value="value"
      @input="$emit('input', $event.target.value)"
    >
  </p>
</template>

<script>
  export default {
    name: "FormInput",

    props: {
      name: {
        type: String,
        required: true,
      },
      label: {
        type: String,
        default: "",
      },
      type: {
        type: String,
        default: "text",
      },
      required: {
        type: Boolean,
        default: false,
      },
      value: {
        type: [ Number, String ],
        default: null,
      },
      disabled: {
        type: Boolean,
        default: false,
      },
    },

    computed: {
      id() {
        return `${ this.name }-${ Date.now().toString(36) }-${ Math.random().toString(36).substr(2) }`;
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../assets/styles/variables";

  input {
    font-size: inherit;
    box-sizing: border-box;
    width: 250px;
    padding: .21em .4em;
    border: 1px solid transparentize(invert($background-color), .2);
    border-radius: 4px;
  }

  abbr {
    font-weight: bold;
    margin-right: .35em;
  }
</style>
