<template>
    <v-app-bar>
        <v-btn v-slot:prepend @click="toHome">Home</v-btn>
        
        <v-btn class="mr-4 ml-auto blurpal" variant="tonal" @click="toAuth">
            <v-icon class="mr-1"><img :src="icon"></v-icon>
            LOGIN
        </v-btn>
    </v-app-bar>
</template>

<script setup>
import icon from '@/assets/DSW.svg'
import router from '@/router';

function toHome() {
    router.push('/')
}

function toAuth() {
    window.location.href = 'https://discord.com/oauth2/authorize?client_id=1343727517529542718&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5173%2Fapi%2Fauth&scope=identify+guilds'
}

</script>

<style scoped>

.blurpal {
    background-color: #5865F2;
    color: white;
}

</style>