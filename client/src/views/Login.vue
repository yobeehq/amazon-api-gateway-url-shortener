<!-- FILE: Login.vue -->
<template>
    <div class="flex items-center justify-center h-screen">
      <div class="px-6 py-10 bg-ambience-0 rounded shadow-md w-80 flex flex-col items-center">
        <img src="/yobee-logo.svg" alt="logo" class="h-6 mb-6">
        <h1 class="font-semibold mb-8">Login to URL Shortener</h1>
        <form @submit.prevent="login" class="flex flex-col gap-4 w-full">
          <div class="w-full">
            <label for="username" class="block text-sm mb-2">Username</label>
            <input type="text" id="username" v-model="username" required placeholder="Enter your username" class="w-full h-12 text-lg px-3 py-2 border rounded appearance-none text-ambience-8 leading-tight focus:outline-none focus:shadow-outline border-ambience-3">
          </div>
          <div class="">
            <label for="password" class="block text-sm mb-2">Password</label>
            <input type="password" id="password" v-model="password" placeholder="Enter your password"  required class="w-full h-12 text-lg px-3 py-2 border rounded appearance-none text-ambience-8 leading-tight focus:outline-none focus:shadow-outline border-ambience-3">
          </div>
          <button type="submit" class="w-full h-12 bg-brand-1 text-ambience-0 rounded font-semibold hover:bg-brand-2">Login</button>
          <p v-if="error" class="mt-3 text-error-1">{{ error }}</p>
        </form>
      </div>
    </div>
</template>


<script>
import axios from 'axios';
export default {
  name: "user-login",
  data() {
    return {
      username: '',
      password: '',
      error: null
    }
  },
  methods: {
    login() {
    //   const oauthTokenBodyJson = {
    //     grant_type: "password",
    //     client_id: process.env.VUE_APP_CLIENT_ID,
    //     username: this.username,
    //     password: this.password
    //   };
    //   const oauthTokenBody = this.convertJSON(oauthTokenBodyJson);

      const oauthTokenBody = new URLSearchParams();
        oauthTokenBody.append('grant_type', 'password');
        oauthTokenBody.append('client_id', process.env.VUE_APP_CLIENT_ID);
        oauthTokenBody.append('username', this.username);
        oauthTokenBody.append('password', this.password);


      axios.post(`${process.env.VUE_APP_AUTH_DOMAIN}/oauth2/token`, oauthTokenBody, {
        ["Content-Type"]: "application/x-www-form-urlencoded",
      })
      .then((response) => {
        let json = response.data;
        if (json.id_token) {
          localStorage.setItem("cognitoIdentityToken", json.id_token);
          localStorage.setItem("cognitoRefreshToken", json.refresh_token);
          this.$store.commit("authorize");
        }
      })
      .catch((error) => {
        this.error = error.message;
        this.$store.commit("deAuthorize");
      });
    },
    convertJSON: function (json) {
      const oAuthTokenBodyArray = Object.entries(json).map(([key, value]) => {
        const encodedKey = encodeURIComponent(key);
        const encodedValue = encodeURIComponent(value);
        return `${encodedKey}=${encodedValue}`;
      });
      return oAuthTokenBodyArray.join("&");
    }
  }
}
</script>