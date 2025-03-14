<template>
    <v-app-bar>
        <template v-slot:prepend>
            <v-app-bar-nav-icon></v-app-bar-nav-icon>
        </template>
        <v-app-bar-title>CupidBot</v-app-bar-title>

        <v-btn @click="toHome">
            <v-icon icon="mdi-robot-love-outline" />
            <span>Home</span>
        </v-btn>

        <v-btn value="Swipe" v-if="loggedIn" @click="toSwipe">
            <v-icon icon="mdi-gesture-swipe" />
            <span>Swipe</span>
        </v-btn>

        <v-btn value="Account" v-if="loggedIn" @click="toSignup">
            <v-icon icon="mdi-account" />
            <span>Account</span>
        </v-btn>

        <v-btn value="Matches" v-if="loggedIn">
            <v-icon icon="mdi-account-check" />
            <span>Matches</span>
        </v-btn>

        <v-btn value="Message" v-if="loggedIn">
            <v-icon icon="mdi-message-text" />
            <span>Message</span>
        </v-btn>

        <v-btn value="Logout" v-if="loggedIn" @click="removeAuth">
            <v-icon icon="mdi-logout"/>
            <span>Logout</span>
        </v-btn>


    </v-app-bar>
</template>

<script setup>
import icon from '@/assets/DSW.svg'
import router from '@/router';
import { inject, onMounted, watch } from 'vue';

const AUTHURL = "https://discord.com/oauth2/authorize?client_id=1343727517529542718&response_type=code&redirect_uri=https%3A%2F%2Fcupidbot.xyz%2Fapi%2F0auth%2Fexchange&scope=identify+guilds+email"
const userProfile = inject('userProfile')
const loggedIn = inject('loggedIn')

function toHome() {
    router.push('/')
}


function removeAuth() {
    console.log('logout')
    fetch('/api/0auth/clear')
    userProfile.value = {}
    loggedIn.value = false
    router.replace('/')
}

function toAuth() {
    window.location.href = AUTHURL
}


function toSignup() {
    router.push('/signup')
}

function toSwipe() {
    router.push('/swipe')
}

</script>


<style scoped>

.blurpal {
    background-color: #5865F2;
    color: white;
}

.container {
    display: flex;
}

button {
    height: 0.5rem;
}

</style>