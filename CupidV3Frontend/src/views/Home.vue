<template>
  <div class="container">
    <div class="home-button">
      <img src="../assets/cupidpfp.jpg" alt="">
      <h1>CupidBot</h1>
      <v-btn>Invite to server</v-btn>
      <v-btn class="blurpal" variant="tonal" v-if="!loggedIn" @click="toAuth">
        <v-icon icon="mdi-login"></v-icon>
        <span>Login With Discord</span>
      </v-btn>
    </div>
    
  </div>
</template>

<script setup>
import { inject, ref } from 'vue';

const loggedIn = inject('loggedIn')
const AUTHURL = "https://discord.com/oauth2/authorize?client_id=1343727517529542718&response_type=code&redirect_uri=https%3A%2F%2Fcupidbot.xyz%2Fapi%2F0auth%2Fexchange&scope=identify+guilds+email"

function toAuth() {
    window.location.href = AUTHURL
}

</script>

<style scoped>

img {
  height: 250px;
  border-radius: 100%;
}

.blurpal {
  background-color: #5865F2;
  color: #E0E3FF
}

.home-button {
  border-radius: 10px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 0.25rem;

  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.448);
}

.container {
  width: 80vw;
  margin: auto;
  margin-top: 8rem;

  display: flex;
  align-items: center;
  justify-content: center;
}
</style>