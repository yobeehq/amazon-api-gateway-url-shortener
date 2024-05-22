<template>
  <div class="flex flex-col h-screen">
    <header v-if="authorized" class="w-full fixed top-0 text-white bg-ambience-0 border-b-[1px] border-b-ambience-2">
      <nav class="container flex items-center justify-between py-6 px-6 mx-auto">
        <img src="/yobee-logo.svg" alt="logo" class="h-4" />
        <h1 class="font-bold text-xl">Private URL Shortener</h1>
        <div></div>
        <!-- <div :class="{ 'block': isOpen, 'hidden': !isOpen }" @click="isOpen = !isOpen" class="cursor-pointer">
          <svg class="fill-current h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"/>
          </svg>
        </div> -->
      </nav>
    </header>
    <main :class="{ 'mt-20': authorized }" class="mb-20 bg-root-0">
      <div class="container mx-auto">
        <router-view />
      </div> 
    </main>
  </div>
</template>

<script>
import { mapState } from "vuex";
import axios from "axios";

// Set Cognito Vars
const clientId = process.env.VUE_APP_CLIENT_ID;
const authDomain = process.env.VUE_APP_AUTH_DOMAIN;
const queryStringParams = new URLSearchParams(window.location.search);
const cognitoCode = queryStringParams.get("code") || null;
const lnf = queryStringParams.get("lnf") || null;
const redUrl = window.location.origin;

export default {
  name: "app",
  data() {
    return {
      appName: `Magic ${process.env.VUE_APP_NAME}`,
      signUpUrl: `${authDomain}/signup?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(redUrl)}`,
      logInUrl: `${authDomain}/login?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(redUrl)}`,
      logOutUrl: `${authDomain}/logout?client_id=${clientId}&logout_uri=${encodeURIComponent(redUrl)}`,
      linkNotFound: lnf,
      isOpen: false,
    };
  },
  created() {
    if (cognitoCode) this.exchangeToken();
    else this.exchangeRefreshToken();
  },
  methods: {
    convertJSON: function (json) {
      const oAuthTokenBodyArray = Object.entries(json).map(([key, value]) => {
        const encodedKey = encodeURIComponent(key);
        const encodedValue = encodeURIComponent(value);
        return `${encodedKey}=${encodedValue}`;
      });
      return oAuthTokenBodyArray.join("&");
    },
    exchangeRefreshToken: function () {
      const oauthTokenBodyJson = {
        grant_type: "refresh_token",
        client_id: clientId,
        refresh_token: localStorage.getItem("cognitoRefreshToken"),
      };
      const oauthTokenBody = this.convertJSON(oauthTokenBodyJson);

      if (oauthTokenBodyJson.refresh_token) {
        return axios
          .post(`${authDomain}/oauth2/token`, oauthTokenBody, {
            ["Content-Type"]: "application/x-www-form-urlencoded",
          })
          .then((response) => {
            let json = response.data;
            if (json.id_token) {
              localStorage.setItem("cognitoIdentityToken", json.id_token);
              this.$store.commit("authorize");
            }
          })
          .catch(() => {
            this.$store.commit("deAuthorize");
          });
      } else {
        return new Promise((res) => {
          return res({});
        });
      }
    },
    exchangeToken: function () {
      const oauthTokenBodyJson = {
        grant_type: "authorization_code",
        client_id: clientId,
        code: cognitoCode,
        redirect_uri: redUrl,
      };
      const oauthTokenBody = this.convertJSON(oauthTokenBodyJson);

      return axios
        .post(`${authDomain}/oauth2/token`, oauthTokenBody, {
          ["Content-Type"]: "application/x-www-form-urlencoded",
        })
        .then((response) => {
          let json = response.data;
          if (json.id_token) {
            localStorage.setItem("cognitoIdentityToken", json.id_token);
            localStorage.setItem("cognitoRefreshToken", json.refresh_token);
            this.$store.commit("authorize");
          }
          let query = Object.assign({}, this.$route.query);
          delete query.code;
          this.$router.replace({ query });
        })
        .catch(() => {
          this.$store.commit("deAuthorize");
        });
    },
    logout: function () {
      localStorage.setItem("cognitoIdentityToken", null);
      localStorage.setItem("cognitoRefreshToken", null);
    },
  },
  computed: {
    ...mapState(["authorized"]),
  },
};
</script>
