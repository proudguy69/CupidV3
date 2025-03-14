<template>
    <v-app-bar>
        <v-btn v-slot:prepend @click="toHome">Home</v-btn>
        
        
        <v-btn size="x-small" class="mr-1 blurpal"  variant="tonal" @click="toAuth" v-if="!userProfile.username">
            <v-icon class="mr-1"><img :src="icon"></v-icon>
            LOGIN
        </v-btn>

        <v-btn size="x-small" class="ml-auto mr-1" variant="tonal" v-if="userProfile.username">
            Swipe (Coming soon)
        </v-btn>

        <v-btn size="x-small" class="mr-1" variant="tonal" @click="toSignup" v-if="userProfile.username">
            Create Account
        </v-btn>

        <v-btn size="x-small" class="bg-error mr-1" variant="tonal" @click="removeAuth" v-if="userProfile.username">
            LOGOUT
        </v-btn>
        
        

        <!--Need to find out if we have a profile or not-->

        

    </v-app-bar>
</template>

<script setup>
import icon from '@/assets/DSW.svg'
import router from '@/router';
import { inject, onMounted, watch } from 'vue';

const AUTHURL = "https://discord.com/oauth2/authorize?client_id=1343727517529542718&response_type=code&redirect_uri=https%3A%2F%2Fcupidbot.xyz%2Fapi%2F0auth%2Fexchange&scope=identify+guilds+email"
const userProfile = inject('userProfile')

function toHome() {
    router.push('/')
}


function removeAuth() {
    console.log('logout')
    fetch('/api/0auth/clear')
    userProfile.value = {}
    router.replace('/')
}

function toAuth() {
    window.location.href = AUTHURL
}


function toSignup() {
    router.push('/signup')
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