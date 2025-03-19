<template>
    <div class="container mx-auto">
        <ProfileCard
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
    </div>
    
</template>

<script setup>
import ProfileCard from '@/components/ProfileCard.vue';
import { inject, onMounted, ref, watch } from 'vue';

const profileData = ref({})
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
let profiles = []

async function match() {
    return
    const response = await fetch(`/api/profiles/${userProfile.value.id}/match`, {
        method:'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(currentProfile.value)
    })
    const response_json = await response.json()
    console.log(response_json)
}

async function reject() {
    setTimeout(async () => {
        profiles = await getProfiles()
        currentProfile.value = getRandomProfile(profiles)
    }, 750);
    

}

watch(userProfile, async (new_profile) => {
    //if (profileData) { return }
    const response = await fetch(`/api/profiles/get/${userProfile.value.id}`)
    const response_json = await response.json()
    profileData.value = JSON.parse(response_json.matching_profile)
    profiles = await getProfiles()
    currentProfile.value = getRandomProfile(profiles)
})

onMounted(async () => {
    if (!userProfile.value.id) {return}
    const response = await fetch(`/api/profiles/get/${userProfile.value.id}`)
    const response_json = await response.json()
    profileData.value = JSON.parse(response_json.matching_profile)
    profiles = await getProfiles()
    currentProfile.value = getRandomProfile(profiles)
})

function getRandomProfile(profiles) {
    const randomIndex = Math.floor(Math.random() * profiles.length);
    return profiles[randomIndex]
}

async function getProfiles() {
    const response = await fetch(`/api/profiles/get/${userProfile.value.id}/compatible`)
    const response_json = await response.json()
    console.log(response_json)
    return response_json.profiles
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