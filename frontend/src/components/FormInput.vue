<template>
  <p>
    <label :for="id">
      <span v-if="label">
        {{ label }}:
        <abbr
          v-if="required"
          :class="$style.abbr"
          title="Required"
        >*</abbr>
      </span>
    </label>
    <input
      :id="id"
      :class="$style.input"
      :disabled="disabled"
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

<style lang="scss" module>
  .input {
    width: 250px;
  }

  .abbr {
    font-weight: bold;
    margin-right: .35em;
  }
</style>
