<template>
  <section :class="$style.container">
    <button
      :class="$style.button"
      :disabled="!prevPage || disabled"
      @click.prevent="handleClick(prevPage)"
    >
      &ltcc;
    </button>
    <button
      :class="$style.button"
      :disabled="value === 1 || disabled"
      @click.prevent="handleClick(1)"
    >
      &#xab;
    </button>
    <button
      v-for="p in pageArray"
      :key="p"
      :class="{ [$style.selected]: p === pageNumber, [$style.button]: true }"
      :disabled="disabled"
      @click.prevent="handleClick(p)"
    >
      {{ p }}
    </button>
    <button
      :class="$style.button"
      :disabled="value === lastPage || disabled"
      @click.prevent="handleClick(lastPage)"
    >
      &#xbb;
    </button>
    <button
      :class="$style.button"
      :disabled="!nextPage || disabled"
      @click.prevent="handleClick(nextPage)"
    >
      &gtcc;
    </button>
  </section>
</template>

<script>
  export default {
    name: "PaginationFooter",

    props: {
      paginationMetadata: {
        type: Object,
        required: true,
      },
      showPages: {
        type: Number,
        default: 5,
      },
      disabled: {
        type: Boolean,
        default: false,
      },
      value: {
        type: Number,
        default: 1,
      },
    },

    computed: {

      prevPage() {
        const { pageNumber } = this;

        if (1 >= pageNumber) {
          return false;
        }

        return pageNumber - 1;
      },

      nextPage() {
        const { pageNumber, lastPage } = this;

        if (lastPage <= pageNumber) {
          return false;
        }

        return pageNumber + 1;
      },

      lastPage() {
        return this.paginationMetadata.total;
      },

      pageNumber() {
        const { value: page, lastPage } = this;

        // Restrict `page` to range [1, `total`]
        return Math.min(lastPage, Math.max(1, page));
      },

      pageArray() {
        const { pageNumber: page, showPages, lastPage: total } = this;

        const getStartAndEnd = () => {
          if (total <= showPages) {
            return { start: 1, end: total };
          }

          const maxPagesBeforeCurrentPage = Math.floor(showPages / 2);
          const maxPagesAfterCurrentPage = Math.ceil(showPages / 2) - 1;

          if (page <= maxPagesBeforeCurrentPage) {
            return { start: 1, end: showPages };
          }

          if (page + maxPagesAfterCurrentPage >= total) {
            return { start: total - showPages + 1, end: total };
          }

          return { start: page - maxPagesBeforeCurrentPage, end: page + maxPagesAfterCurrentPage };
        };

        const { start, end } = getStartAndEnd();

        return Array(end - start + 1).fill(0).map((_, i) => i + start);
      },
    },

    methods: {

      handleClick(page) {
        this.$emit("input", page);
      },

    },
  };
</script>

<style lang="scss" module>
  @import "../assets/styles/variables";

  .container {
    display: flex;
    align-items: end;
    justify-content: center;
  }

  .button {
    font-size: 100%;
    margin: 0 .3em;
    padding: 0;
    user-select: none;
    color: $link-color;
    border: none;
    background: none;

    &:hover {
      color: $link-color-active;
    }
  }

  .selected {
    font-weight: bold;
  }
</style>
