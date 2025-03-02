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


async function loadAccess() {
    const response = await fetch('/api/get/access')
    const response_json = await response.json()
    return response_json
}

onMounted(async () => {
    
    const accessData = await loadAccess()
    //console.log(accessData)
    
    token.value = accessData
    
    
})

provide('token', token)



</script>

<style>



</style>