<template>
    <v-app>
        <Navigation/>
        <router-view></router-view>
    </v-app>
</template>

<script setup>
import { onMounted, provide, ref } from 'vue';
import Navigation from './components/Navigation.vue';


const userProfile = ref({})

async function loadProfile() {
    const response = await fetch('/api/0auth/profile')
    const response_json = await response.json()
    return response_json
}

onMounted(async () => {
    
    const profileData = await loadProfile()
    if (profileData.success) {
        userProfile.value = profileData.profile
    }

    
    
})

provide("userProfile", userProfile)



</script>

<style>



</style>