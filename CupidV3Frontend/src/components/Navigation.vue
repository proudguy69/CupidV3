<template>
    <v-app-bar>
        <v-btn v-slot:prepend @click="toHome">Home</v-btn>
        
        <v-btn class="mr-4 ml-auto blurpal" variant="tonal" @click="toAuth" v-if="!token.success">
            <v-icon class="mr-1"><img :src="icon"></v-icon>
            LOGIN
        </v-btn>

        <v-btn class="ml-auto mr-4" variant="tonal" @click="toSignup" v-if="token.success">
            Create Account
        </v-btn>

        <v-btn class="bg-error mr-4" variant="tonal" @click="removeAuth" v-if="token.success">
            LOGOUT
        </v-btn>

        <!--Need to find out if we have a profile or not-->

        

    </v-app-bar>
</template>

<script setup>
import icon from '@/assets/DSW.svg'
import router from '@/router';
import { inject, onMounted, watch } from 'vue';


const token = inject('token')

function toHome() {
    router.push('/')
}



function removeAuth() {
    fetch('/api/logout')
    token.value = {}
    router.replace('/')
}



function toAuth() {
    window.location.href = 'https://discord.com/oauth2/authorize?client_id=1343727517529542718&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5173%2Fapi%2Fauth&scope=identify+guilds'
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

</style>