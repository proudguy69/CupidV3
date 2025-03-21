<template>
    <v-app>
        <Navigation v-if="!mobile"/>
        <router-view></router-view>
        <MobileNavigation v-if="mobile"/>
    </v-app>
</template>

<script setup>
import { onMounted, provide, ref } from 'vue';
import Navigation from './components/Navigation.vue';
import MobileNavigation from './components/MobileNavigation.vue';

const mobile = ref(false)
const superMobile = ref(false)
const userProfile = ref({})
const loggedIn = ref(false)
const dev_uri = 'https://discord.com/oauth2/authorize?client_id=1343727517529542718&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5173%2Fapi%2F0auth%2Fexchange&scope=identify+guilds+email'
const prod_uri = 'https://discord.com/oauth2/authorize?client_id=1343727517529542718&response_type=code&redirect_uri=https%3A%2F%2Fcupidbot.xyz%2Fapi%2F0auth%2Fexchange&scope=identify+guilds+email'
const dev = false
const oauth_uri = ref('')

if (dev) {
    oauth_uri.value = dev_uri
} else {
    oauth_uri.value = prod_uri
}

provide('oauth_uri', oauth_uri)

async function loadProfile() {
    const response = await fetch('/api/0auth/profile')
    const response_json = await response.json()
    return response_json
}

window.addEventListener('resize', () => {
    if (window.innerWidth <= 850 &&  window.innerWidth > 500) {
        mobile.value = true
        superMobile.value = false   
    }
    if (window.innerWidth <= 500) {
        superMobile.value = true
    }
    if (window.innerWidth > 850) {
        mobile.value = false
    }
})

onMounted(async () => {
    if (window.innerWidth <= 850 ) {
        mobile.value = true
    }
    if (window.innerWidth <= 500) {
        superMobile.value = true
    }
    const profileData = await loadProfile()
    if (profileData.success) {
        userProfile.value = profileData.profile
        loggedIn.value = true
    }

    
    
})

provide("userProfile", userProfile)
provide('loggedIn', loggedIn)
provide('superMobile', superMobile)



</script>

<style>



</style>