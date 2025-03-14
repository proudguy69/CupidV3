<template>
    <v-app>
        <!--<Navigation/>-->
        <router-view></router-view>
        <MobileNavigation/>
    </v-app>
</template>

<script setup>
import { onMounted, provide, ref } from 'vue';
import Navigation from './components/Navigation.vue';
import MobileNavigation from './components/MobileNavigation.vue';


const userProfile = ref({})
const loggedIn = ref(false)

async function loadProfile() {
    const response = await fetch('/api/0auth/profile')
    const response_json = await response.json()
    return response_json
}

onMounted(async () => {
    
    const profileData = await loadProfile()
    if (profileData.success) {
        userProfile.value = profileData.profile
        loggedIn.value = true
    }

    
    
})

provide("userProfile", userProfile)
provide('loggedIn', loggedIn)



</script>

<style>



</style>