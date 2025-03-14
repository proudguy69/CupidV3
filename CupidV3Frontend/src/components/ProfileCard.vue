
<template>
    <v-card class="card" :class="{active : active, 'bg-success':green, 'bg-error':red}">
        <v-img
            :src="banner_url"
            cover
            class="text-white">

            <v-card-title>
                <div class="card-title">
                    <img class="icon" :src="avatar_url"></img>
                    <span class="name">{{ profile_name }}</span>
                </div>
                <v-chip>{{ profile_age }}</v-chip>
                <v-chip class="ml-3">{{ profile_gender }}</v-chip>
                <v-chip class="ml-3">{{ profile_pronouns }}</v-chip>
                <v-chip class="ml-3">{{ profile_sexuality }}</v-chip>
                
            </v-card-title>
        </v-img>
        
        <v-card-text>
            {{ profile_username }}
        </v-card-text>
        
        <v-card-text :class="{hidden : !active}">
            {{ profile_bio }}
        </v-card-text>
    <div class="buttons">
        <v-btn variant="tonal" class="bg-error" @click="reject"><- Reject</v-btn>
        <v-btn variant="tonal" class="bg-success" @click="match">Match -></v-btn>
    </div>
    
    </v-card>
</template>

<script setup>
import { onMounted, ref } from 'vue';

const props = defineProps({
    avatar_url:String,
    banner_url:String,
    profile_name:String,
    profile_username:String,
    profile_age:Number,
    profile_pronouns:String,
    profile_gender:String,
    profile_sexuality:String,
    profile_bio:String
})

const active = ref(true)
const green = ref(false)
const red = ref(false)


onMounted(() => {
    setTimeout(() => {
        active.value = true
    }, 1000);
})

async function match() {
    green.value = true

    setTimeout(() => {
        active.value = false
        green.value = false
    }, 500);

    setTimeout(() => {
        active.value = true
    }, 1000);
}

async function reject() {
    red.value = true

    setTimeout(() => {
        active.value = false
        red.value = false
    }, 500);

    setTimeout(() => {
        active.value = true
    }, 1000);
}

</script>


<style>

.buttons {
    display: flex;
    justify-content: space-between;
    padding: 1rem;
}

.icon {
    height: 48px;
    border-radius: 100px;
}

.card-title {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    margin-bottom: 4px;
}

.v-chip {
  background-color: rgba(0, 0, 0, 0.85) !important; /* Less transparent */
  color: white !important;
}

.name {
    padding-left: 6px;
    padding-right: 6px;
    background-color: rgba(0, 0, 0, 0.65);
    border-radius: 10px;
}

.card {
    width: 400px;
    transition: all 1s;
    opacity: 0;
}

.card.active {
    transition: all 1s;
    opacity: 1;
}

</style>