<template>
    <v-app-bar>
        <v-btn v-slot:prepend @click="toHome">Home</v-btn>
        
        <v-btn class="mr-4 ml-auto blurpal" variant="tonal">
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

</script>

<style scoped>

.blurpal {
    background-color: #5865F2;
    color: white;
}

</style>