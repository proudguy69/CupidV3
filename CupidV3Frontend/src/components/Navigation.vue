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

        <v-btn value="login" v-if="!loggedIn" @click="toAuth">
            <v-icon icon="mdi-login"/>
            <span>Login</span>
        </v-btn>

        <v-btn value="Swipe" v-if="loggedIn" @click="toSwipe">
            <v-icon icon="mdi-gesture-swipe" />
            <span>Swipe</span>
        </v-btn>

        <v-btn value="Account" v-if="loggedIn" @click="toSignup">
            <v-icon icon="mdi-account" />
            <span>Account</span>
        </v-btn>

        <v-btn value="Matches" v-if="loggedIn" @click="toMatches">
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
import { toAuth, toHome, toSignup, toSwipe, removeAuth, toMatches } from '@/utils/navigation';
import { inject, onMounted, watch } from 'vue';

const oauth_uri = inject('oauth_uri')
const userProfile = inject('userProfile')
const loggedIn = inject('loggedIn')


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