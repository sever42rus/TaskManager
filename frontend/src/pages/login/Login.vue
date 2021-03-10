<template>
  <div class="container h-100">
    <div class="h-100 row justify-content-md-center align-items-center">
      <div class="col-6">
        <form class="card" v-on:submit.prevent="loginSubmit">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">Авторизация</h2>
            <div class="mb-3">
              <label class="form-label">Email адрес</label>
              <input
                type="email"
                :class="{ 'is-invalid': formError.email }"
                class="form-control"
                placeholder="Enter email"
                v-model.trim="email"
              />
            </div>
            <div class="mb-2">
              <label class="form-label"> Пароль </label>
              <input
                type="password"
                :class="{ 'is-invalid': formError.password }"
                class="form-control"
                placeholder="Password"
                autocomplete="off"
                v-model.trim="password"
              />
            </div>
            <div class="text-center">
              <div class="m-4">
                <button
                  type="button"
                  v-on:click="loginSubmit"
                  class="btn btn-primary w-50"
                >
                  Войти
                </button>
              </div>
              <div class="m-4">
                <router-link class="btn btn-primary w-50" to="recovery-pass"
                  >Восстановить пароль</router-link
                >
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "Login",
  components: {},
  data: () => ({
    email: "",
    password: "",
    error: "",
    formError: Object,
  }),
  methods: {
    async loginSubmit() {
      const response = await fetch("/auth/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: this.email,
          password: this.password,
        }),
      });
      if (response.ok) {
        var data = await response.json();
        localStorage.setItem("userIni", data.ini);
        localStorage.setItem("authStatus", true);
        this.$router.push({ name: "home" }).catch(() => {});
      } else {
        if (response.status == "400") this.error = "Неверный логин или пароль";
        else if (response.status == "500") this.error = "Ошибка API";
        else {
          this.error = "Неизвестная ошибка";
        }
      }
    },
  },
};
</script>

<style>
</style>