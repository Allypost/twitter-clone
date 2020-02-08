<template>
  <form @submit="handleSubmit" action="/api/auth/login" method="post">
    <h1>Login</h1>
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
        label="Remember me"
        name="remember-me"
        type="checkbox"
        v-model="inputs.rememberMe"
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
        value="Login"
      />
    </section>
  </form>
</template>

<script>
  import FormInput from "@/components/FormInput";

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

      async handleSubmit(e) {
        e.preventDefault();

        this.$set(this, "submitError", "");

        this.$set(this, "posting", true);
        const { success, errors, data } = await this.$post("/api/auth/login", this.inputs);
        this.$set(this, "posting", false);

        this.$set(this, "submitError", errors.join(" "));

        if (success) {
          this.$store.commit("user/setUser", data);
          await this.$router.push({ name: "Home" });
        }
      },

    },
  };
</script>
