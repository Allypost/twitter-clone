<template>
  <section>
    <label>
      Filter:
      <select
        v-model="filter"
        :disabled="$attrs.disabled || false"
      >
        <option
          v-for="option in filterOptions"
          :key="option"
          :value="option"
        >{{ option | capitalize }}
        </option>
      </select>
    </label>

    <template
      v-if="filter !== filterOptions.none"
    >
      <span :class="$style.spacer" />

      <template
        v-if="filter === filterOptions.before"
      >
        <NiceDateTime
          v-model="dates.before"
          v-bind="{
            ...$attrs,
            class: $style.datetime,
            inputClass: $style.datetimeInput
          }"
        />
      </template>

      <template
        v-if="filter === filterOptions.after"
      >
        <NiceDateTime
          v-model="dates.after"
          v-bind="{
            ...$attrs,
            class: $style.datetime,
            inputClass: $style.datetimeInput
          }"
        />
      </template>

      <template
        v-if="filter === filterOptions.between"
      >
        <NiceDateTime
          v-model="dates.after"
          v-bind="{
            ...$attrs,
            class: $style.datetime,
            inputClass: $style.datetimeInput
          }"
        />
        <span>
          and
        </span>
        <NiceDateTime
          v-model="dates.before"
          v-bind="{
            ...$attrs,
            class: $style.datetime,
            inputClass: $style.datetimeInput,
            minDatetime: dates.before || null
          }"
        />
      </template>
    </template>
  </section>
</template>

<script>
  import NiceDateTime from "@/components/datetime/NiceDateTime";

  const filterOptions = Object.fromEntries(
    [
      "none",
      "before",
      "after",
      "between",
    ]
      .map((a) => [ a, a ]),
  );

  export default {
    name: "DateTimePicker",

    components: { NiceDateTime },

    filters: {

      capitalize(string) {
        if (!string) {
          return "";
        }

        string = String(string);

        return string.charAt(0).toUpperCase() + string.slice(1);
      },

    },

    inheritAttrs: false,

    props: {
      value: {
        type: Object,
        required: true,
      },
    },

    data: () => ({
      filterOptions,
      filter: filterOptions.none,
      dates: {
        before: "",
        after: "",
      },
    }),

    watch: {

      filter(val) {
        switch (val) {
          case filterOptions.none:
            this.$set(this.dates, "before", "");
            this.$set(this.dates, "after", "");
            break;
          case filterOptions.before:
            this.$set(this.dates, "after", "");
            break;
          case filterOptions.after:
            this.$set(this.dates, "before", "");
            break;
        }
      },

      dates: {
        deep: true,
        handler({ before, after }) {
          const { filter, filterOptions } = this;

          if (filter !== filterOptions.between) {
            return this.$emit("input", { before, after });
          }

          if (!(before.length && after.length)) {
            return;
          }

          this.$emit("input", { before, after });
        },
      },

    },

  };
</script>

<style lang="scss" module>
  @import "../assets/styles/variables";

  .spacer {
    margin: 0 .2em;
  }

  .datetime {
    display: inline-block;
  }

  .datetime-input {
    text-align: center;
  }
</style>
