<template>
  <form
    action="/api/auth/login"
    method="post"
    @submit.prevent="handleSubmit"
  >
    <h1>Login</h1>
    <section :class="$style.loginContainer">
      <FormInput
        v-model="inputs.username"
        :disabled="posting"
        label="Username"
        name="username"
        required
      />
      <FormInput
        v-model="inputs.password"
        :disabled="posting"
        label="Password"
        name="password"
        required
        type="password"
      />
      <FormInput
        v-model="inputs.rememberMe"
        :disabled="posting"
        label="Remember me"
        name="remember-me"
        type="checkbox"
      />
      <p
        v-if="inputError"
        :class="$style.inputError"
      >
        <span>{{ inputError }}</span>
      </p>
      <p
        v-if="submitError"
        :class="$style.inputError"
      >
        <span>{{ submitError }}</span>
      </p>
      <FormInput
        :disabled="!canSubmit"
        name="submit"
        style="cursor: pointer"
        type="submit"
        value="Login"
      />
    </section>
  </form>
</template>

<script>
  import FormInput from "@/components/FormInput";
  import { mapActions } from "vuex";

  export default {
    name: "Login",

    components: { FormInput },

    data: () => ({
      inputs: {
        username: "",
        password: "",
        rememberMe: false,
      },
      posting: false,
      submitError: "",
    }),

    computed: {

      inputError() {
        if (this.posting) {
          return "";
        }

        const inputFilled = (inputValue) => {
          switch (typeof inputValue) {
            case "string":
              return 0 < inputValue.length;
            case "boolean":
              return true;
            default:
              return true;
          }
        };

        const inputsFilled = Object
          .values(this.inputs)
          .reduce((acc, inputValue) => acc && inputFilled(inputValue), true)
        ;

        if (!inputsFilled) {
          return "You must fill in all the fields.";
        }

        return "";
      },

      canSubmit() {
        if (this.posting) {
          return false;
        }

        return "" === this.inputError;
      },

    },

    methods: {

      async handleSubmit() {
        this.$set(this, "submitError", "");

        this.$set(this, "posting", true);
        const error = await this.login(this.inputs);
        this.$set(this, "posting", false);

        if (error) {
          this.$set(this, "submitError", error);
        } else {
          await this.$router.push({ name: "Home" });
        }
      },

      ...mapActions({
        "login": "user/login",
      }),

    },

  };
</script>

<style lang="scss" module>
  .login-container {
    font-size: 120%;
    display: inline-block;
    margin: 0 auto;
    text-align: right;
  }

  .input-error {
    font-size: 80%;
    color: #b71c1c;
  }
</style>
