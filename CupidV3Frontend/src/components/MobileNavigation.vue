<template>
    <v-bottom-navigation grow horizontal>

        <v-btn value="Home" @click="toHome" size="x-small">
            <v-icon icon="mdi-robot-love-outline" />
            <span>Home</span>
        </v-btn>

        <v-btn value="Login" v-if="!loggedIn" @click="toAuth" size="x-small">
            <v-icon icon="mdi-login"/>
            <span>Discord Login</span>
        </v-btn>

        <v-btn value="Swipe" v-if="loggedIn" @click="toSwipe" size="x-small">
            <v-icon icon="mdi-gesture-swipe" />
            <span>Swipe</span>
        </v-btn>

        <v-btn value="Account" v-if="loggedIn" @click="toSignup" size="x-small">
            <v-icon icon="mdi-account" />
            <span>Account</span>
        </v-btn>

        <v-btn value="Matches" v-if="loggedIn" size="x-small">
            <v-icon icon="mdi-account-check" />
            <span>Matches</span>
        </v-btn>

        <v-btn value="Message" v-if="loggedIn" size="x-small">
            <v-icon icon="mdi-message-text" />
            <span>Message</span>
        </v-btn>

        <v-btn value="Logout" v-if="loggedIn" @click="removeAuth" size="x-small">
            <v-icon icon="mdi-logout"/>
            <span>Logout</span>
        </v-btn>

    </v-bottom-navigation>
</template>

<script setup>
import router from '@/router';
import { ref, inject } from 'vue';
const AUTHURL = "https://discord.com/oauth2/authorize?client_id=1343727517529542718&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5173%2Fapi%2F0auth%2Fexchange&scope=identify+guilds+email"


const loggedIn = inject('loggedIn')
const userProfile = inject('userProfile')


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

<style>

span {
    font-size: x-small;
}
</style>