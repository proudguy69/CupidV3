<template>
    <v-app>
        <Navigation/>
        <router-view></router-view>
    </v-app>
</template>

<script setup>
import { onMounted, provide, ref } from 'vue';
import Navigation from './components/Navigation.vue';

const token = ref({})
const user_data = ref({})


async function loadAccess() {
    const response = await fetch('/api/get/access')
    const response_json = await response.json()
    return response_json
}

async function loadDiscordProfile(token_data) {
    const headers = {"Authorization": `${token_data.token_type} ${token_data.access_token}`,"Content-Type":'application/json'}
    const uri = 'https://discord.com/api/users/@me'
    const response = await fetch(uri, {headers:headers})
    const response_json = await response.json()
    if (response.status != 200) {return}
    user_data.value = response_json
}

onMounted(async () => {
    
    const accessData = await loadAccess()

    token.value = accessData
    loadDiscordProfile(token.value.token_data)
    
    
})

provide('token', token)
provide('user_data', user_data)



</script>

<style>



</style>