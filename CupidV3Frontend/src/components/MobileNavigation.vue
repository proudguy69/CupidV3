<template>
    <v-bottom-navigation grow horizontal>

        <v-btn value="Home" @click="toHome" size="x-small">
            <v-icon icon="mdi-robot-love-outline" />
            <span>Home</span>
        </v-btn>

        <v-btn value="otherlogin" v-if="!loggedIn" @click="toAuth" size="x-small">
            <v-icon icon="mdi-login"/>
            <span>Discord Login</span>
        </v-btn>
        
        <v-btn value="Swipe" v-if="loggedIn" @click="toSwipe" size="x-small">
            <v-icon icon="mdi-gesture-swipe" />
            <span>Swipe</span>
        </v-btn>

        <v-btn value="Account" v-if="loggedIn && !superMobile" @click="toSignup" size="x-small">
            <v-icon icon="mdi-account" />
            <span>Account</span>
        </v-btn>

        <v-menu v-if="loggedIn && superMobile">
            <template v-slot:activator="{ props }">
                <v-btn v-bind="props" size="x-small">
                    <v-icon icon="mdi-account" />
                    <span>Account Menu</span>
                </v-btn>
            </template>
            <v-list>
                <v-list-item>
                    <v-btn variant="text" @click="toSignup"> 
                        <v-icon icon="mdi-account" />
                        <span>Account</span>
                    </v-btn>
                </v-list-item>
                <v-list-item>
                    <v-btn variant="text">
                        <v-icon icon="mdi-account-check" />
                        <span>Matches</span>
                    </v-btn>
                </v-list-item>
                <v-list-item>
                    <v-btn variant="text">
                        <v-icon icon="mdi-message-text" />
                        <span>Message</span>
                    </v-btn>
                </v-list-item>
            </v-list>
        </v-menu>
        

        <v-btn value="Matches" v-if="loggedIn && !superMobile" size="x-small">
            <v-icon icon="mdi-account-check" />
            <span>Matches</span>
        </v-btn>

        <v-btn value="Message" v-if="loggedIn  && !superMobile" size="x-small">
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

const loggedIn = inject('loggedIn')
const userProfile = inject('userProfile')
const superMobile = inject('superMobile')
const oauth_uri = inject('oauth_uri')


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
    window.location.href = oauth_uri.value
}


function toSignup() {
    router.push('/signup')
}

function toSwipe() {
    router.push('/swipe')
}

</script>

<style scoped>

span {
    font-size: x-small;
}
</style>