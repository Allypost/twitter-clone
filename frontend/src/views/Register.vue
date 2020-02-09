<template>
  <form @submit="handleSubmit" action="/api/auth/register" method="post">
    <h1>Register</h1>
    <section class="register-container">
      <FormInput
        :disabled="posting"
        label="Username"
        name="username"
        required
        v-model="inputs.username"
      />
      <FormInput
        :disabled="posting"
        label="Password"
        name="password"
        required
        type="password"
        v-model="inputs.password"
      />
      <FormInput
        :disabled="posting"
        label="Repeat password"
        name="password-repeat"
        required
        type="password"
        v-model="inputs.passwordRepeat"
      />
      <p v-if="inputError">
        <span class="input-error">{{ inputError }}</span>
      </p>
      <p v-if="submitError">
        <span class="input-error">{{ submitError }}</span>
      </p>
      <FormInput
        :disabled="!canSubmit"
        name="submit"
        style="cursor: pointer"
        type="submit"
        value="Register"
      />
    </section>
  </form>
</template>

<script>
  import FormInput from "@/components/FormInput";
  import { mapActions } from "vuex";

  export default {
    name: "Register",

    components: { FormInput },

    data: () => ({
      inputs: {
        username: "",
        password: "",
        passwordRepeat: "",
      },
      posting: false,
      submitError: "",
    }),

    computed: {

      inputError() {
        if (this.posting) {
          return "";
        }

        const inputsFilled = Object
          .values(this.inputs)
          .reduce((acc, input) => acc && 0 < input.length, true)
        ;

        if (!inputsFilled) {
          return "You must fill in all the inputs";
        }

        const { password, passwordRepeat } = this.inputs;

        const passwordTooShort = 8 > password.length;

        if (passwordTooShort) {
          return "Your password must be at least 8 characters";
        }

        const passwordTooLong = 2048 < password.length;

        if (passwordTooLong) {
          return "Your password must be shorter than 2048 characters";
        }

        const passwordsMatch = password === passwordRepeat;

        if (!passwordsMatch) {
          return "The passwords must match";
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

      async handleSubmit(e) {
        e.preventDefault();

        this.$set(this, "submitError", "");

        this.$set(this, "posting", true);
        const error = await this.register(this.inputs);
        this.$set(this, "posting", false);

        if (error) {
          this.$set(this, "submitError", error);
        } else {
          await this.$router.push({ name: "Home" });
        }
      },

      ...mapActions({
        "register": "user/register",
      }),

    },
  };
</script>

<style lang="scss" scoped>
  .register-container {
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
