<template>
    <div class="container mx-auto">
        <ProfileCard v-if="prof"
        :avatar_url="currentProfile.avatar_url"
        :banner_url="currentProfile.banner_url"
        :profile_name="currentProfile.name"
        :profile_age="currentProfile.age"
        :profile_pronouns="currentProfile.pronouns"
        :profile_gender="currentProfile.gender"
        :profile_sexuality="currentProfile.sexuality"
        :profile_username="currentProfile.username"
        :profile_bio="currentProfile.bio"
        @match="match"
        @reject="reject"
        />
        <h1 v-if="!prof">All out of matches!</h1>
    </div>
    <v-snackbar :timeout="delay" v-model="snackbar">{{ message }}</v-snackbar>
</template>

<script setup>
import ProfileCard from '@/components/ProfileCard.vue';
import { inject, onMounted, ref, watch } from 'vue';

const message = ref('')
const delay = ref(1000)
const snackbar = ref(false)
const prof = ref(false)

const userProfile = inject('userProfile')
const currentProfile = ref({
    avatar_url:'N/A',
    banner_url:'N/A',
    avatar_hash:'N/A',
    banner_hash:'N/A',
    profile_name:'N/A',
    profile_age:'N/A',
    profile_pronouns:'N/A',
    profile_gender:'N/A',
    profile_sexuality:'N/A',
    profile_username:'N/A',
    profile_bio:'N/A'
})


async function getDiscordUser(user_id) {
    // used for getting a user object for things like banner and what not
    const response = await fetch(`/api/users/partial/${user_id}`)
    const response_data = await response.json()
    return response_data.profile
}

async function match() {
    const response = await fetch(`/api/profiles/${userProfile.value.id}/match/${currentProfile.value.user_id}`, {
        method:'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(currentProfile.valueå)
    })
    const response_json = await response.json()
    if (response_json.success) {
        if (response_json.matched) {
            message.value = "You succesfully matched! its up to you to dm / add them on discord"
            snackbar.value = true
        }
        setTimeout(async ()=> {
            await getProfile() // get a new profile
        }, 750)
        
    }
    console.log(response_json)
}

async function reject() {
    setTimeout(async () => {
        const response = await fetch(`/api/profiles/${userProfile.value.id}/reject/${currentProfile.value.user_id}`, {
            method:'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(currentProfile.value)
        })
        const response_json = await response.json() 
        if (response_json.success) {
            await getProfile() // get a new profile
    }
        console.log(response_json)
    }, 750);
    

}

watch(userProfile, async (new_profile) => {
    await loadProfile()
})

onMounted(async () => {
    await loadProfile()
})

async function loadProfile() {
    if (!userProfile.value.access_token) { return}
    const profile = await getProfile()
    if (!profile) {return}
    const discord_profile = await getDiscordUser(profile.user_id)
    if (discord_profile.avatar) {
        currentProfile.value.avatar_url = `https://cdn.discordapp.com/avatars/${profile.user_id}/${discord_profile.avatar}.png`
    }
    if (discord_profile.banner) {
        currentProfile.value.banner_url = `https://cdn.discordapp.com/banners/${profile.user_id}/${discord_profile.banner}.png`
    }
        
    currentProfile.value = profile
}

async function getProfile() {
    if (!userProfile.value.id) {return}
    const response = await fetch(`/api/profiles/get/${userProfile.value.id}/compatible`)
    const response_json = await response.json()
    // Check and submit toast if needed
    if (!response_json.success) {
        prof.value = false
        setSnackbar(response_json.message, 3000)
        return
    }
    prof.value = true
    currentProfile.value = response_json.profile
    return response_json.profile
}

async function setSnackbar(msg,dly) {
    message.value = msg
    delay.value = dly
    snackbar.value = true
}

</script>

<style scoped>

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

.container {
    height: 100vh;
    width: 100vw;
    display: flex;
    align-items: center;
    justify-content: center;
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

</style>