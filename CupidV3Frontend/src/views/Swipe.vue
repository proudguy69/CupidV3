<template>
    <div class="container mx-auto">
        <ProfileCard
        :avatar_url="profileData.avatar_url"
        :banner_url="profileData.banner_url"
        :profile_name="profileData.name"
        :profile_age="profileData.age"
        :profile_pronouns="profileData.pronouns"
        :profile_gender="profileData.gender"
        :profile_sexuality="profileData.sexuality"
        :profile_username="profileData.username"
        :profile_bio="profileData.bio"
        />
    </div>
    
</template>

<script setup>
import ProfileCard from '@/components/ProfileCard.vue';
import { inject, onMounted, ref, watch } from 'vue';

const profileData = ref({})
const userProfile = inject('userProfile')

watch(userProfile, async (new_profile) => {
    //if (profileData) { return }
    const response = await fetch(`/api/profiles/get/${userProfile.value.id}`)
    const response_json = await response.json()
    profileData.value = JSON.parse(response_json.matching_profile)
    console.log(profileData.value)
})

onMounted(async () => {
    if (!userProfile.value.id) {return}
    const response = await fetch(`/api/profiles/get/${userProfile.value.id}`)
    const response_json = await response.json()
    profileData.value = JSON.parse(response_json.matching_profile)
    console.log(profileData.value)
})

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