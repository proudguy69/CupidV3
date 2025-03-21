<template>
    <div class="container">
        <v-form ref="form" class="top-form" @submit.prevent="submitForm" v-if="userProfile.username">
            <v-text-field
            label="Name"
            v-model="name"
            :rules="nameRules"
            />

            <v-select
            label="Age"
            v-model="age"
            :items="ageOptions"
            :rules="selectRules"
            />

            <v-text-field
            v-if="age == '26+'"
            label="Age Specified"
            v-model="ageSpecified"
            :rules="ageRules"
            />

            <v-text-field
            label="Pronouns"
            v-model="pronouns"
            :rules="pronounRules"
            />

            <v-select
            label="Gender"
            v-model="gender"
            :items="genderOptions"
            :rules="selectRules"
            />

            <v-text-field
            v-if="gender=='Other'"
            label="Gender (Specify)"
            v-model="genderSpecified"
            :rules="genderRules"
            />

            <v-select
            label="Sexuality"
            v-model="sexuality"
            :items="sexualityOptions"
            :rules="selectRules"
            />

            <v-textarea
            label="Bio"
            v-model="bio"
            :rules="bioRules"
            />

            <v-btn class="bg-success" type="submit">Submit Profile</v-btn>
            <v-btn class="bg-error ml-8" @click="deleteProfile">Delete Profile</v-btn>
        </v-form>
        
        <v-form class="filters-form" v-if="userProfile.username">
            <h1>Filters</h1>
            <v-label>Age Filter</v-label>
            <Slider v-model="filters.age"/>
            <v-select
            chips
            label="Gender Filter"
            :items="genderFilterOptions"
            v-model="filters.gender"
            multiple
            />

            <v-select
            chips
            label="Sexuality Filter"
            :items="sexualityOptions"
            v-model="filters.sexuality"
            multiple
            />

            <v-btn @click="submitFilters">
                Save Filters
            </v-btn>
        </v-form>

        <h1 v-if="!userProfile.username">YOU ARENT LOGGED IN TO DISCORD!</h1>
        <p v-if="!userProfile.username">Go to home -> discord login</p>
        
    </div>
    <v-snackbar
        v-model="snackbar"
        :timeout="2000"
        >
        {{ text }}
    </v-snackbar>
</template>

<script setup>
import router from '@/router';
import { computed, inject, onMounted, ref, watch } from 'vue';
import Slider from '@/components/Slider.vue';

const userProfile = inject('userProfile')



const form = ref(null)

const name = ref('')
const age = ref(16)
const ageSpecified = ref('')
const pronouns = ref('')
const gender = ref('Select')
const genderSpecified = ref('')
const sexuality = ref('Select')
const bio = ref('')

const filters = ref({
    age:[age.value-2, age.value+2],
    gender:[],
    sexuality:[]
})

// snackbar stuff
const snackbar = ref(false)
const text = ref('Error Occured')


// options stuff
const genderOptions = ref([
    'Male',
    'Female',
    'Other'
])

const sexualityOptions = ref([
    'Heterosexual',
    'Homosexual',
    'Bisexual',
    'Pansexual',
    'Asexual'
])

const ageOptions = ref([
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    "26+"
])

const genderFilterOptions = ref([
    'Male',
    'Female',
    'Other'
])




// validation rules
const nameRules = ref([
    function characterLimit(value) {
        if (value.length >=3 && value.length <= 20) return true
        return 'Name must be between 3 and 20 characters'
    }
])

const ageRules = ref([
    function characterLimit(value) {
        if (value.length == 2) return true
        return 'must be a valid age'
    }
])

const pronounRules = ref([
    function characterLimit(value) {
        if (value.length >=4 && value.length <= 16) return true
        return 'Pronouns must be between 4 and 16 characters'
    }
])

const genderRules = ref([
    function characterLimit(value) {
        if (value.length >=4 && value.length <= 16) return true
        return 'Pronouns must be between 4 and 16 characters'
    }
])

const selectRules = ref([
    function needSelect(value) {
        if (value != 'Select') return true
        return 'You need to select an option'
    }
])

const bioRules = ref([
    function needSelect(value) {
        if (value.length >= 256) return true
        return `Your bio needs to be 256 or more characters. | ${256-value.length} more needed`
    }
])


async function submitFilters() {
    text.value = "Submitting Filters..."
    snackbar.value = true
    await fetch(`/api/profiles/filters/update/${userProfile.value.id}`,{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify(filters.value)
    })
    text.value = "Filters applied!"
    snackbar.value = true
}

async function get_matching_profile() {
    if (!userProfile.value.id) { return }
    const response = await fetch(`/api/profiles/get/${userProfile.value.id}`)
    const response_json = await response.json()
    if (!response_json.success) { return }
    const profile = JSON.parse(response_json.matching_profile)
    name.value = profile.name
    age.value = profile.age
    pronouns.value = profile.pronouns
    sexuality.value = profile.sexuality
    gender.value = profile.gender
    bio.value = profile.bio
    console.log(profile)
    filters.value.age = profile.filters.age
    filters.value.gender = profile.filters.gender
    filters.value.sexuality = profile.filters.sexuality

}

onMounted(async () => {
    get_matching_profile()
})

watch(userProfile, (new_pr) => {
    get_matching_profile()
})

async function deleteProfile() {
    const response = await fetch(`/api/profiles/delete/${userProfile.value.id}`)
    const response_json = await response.json()
    console.log(response_json)
}

async function submitForm() {
    await form.value.validate()
    if (!form.value.isValid) {return}
    if (!userProfile.value.id) {
        text.value = "You have no ID! please re-log in, go to the home page, THEN go to the signup page"
        snackbar.value = true
        return
    }
    text.value = "Submitting Form..."
    snackbar.value = true



    const data = JSON.stringify({
        user_id:userProfile.value.id,
        name:name.value,
        age: age.value,
        age_specified: ageSpecified.value,
        pronouns:pronouns.value,
        gender:gender.value,
        gender_specified:genderSpecified.value,
        sexuality:sexuality.value,
        bio:bio.value,
        username:userProfile.value.username
    })

    

    const response = await fetch(`/api/profiles/update/${userProfile.value.id}`, {
        method: 'POST',
        headers: {"Content-Type":'application/json'},
        body: data
    })

    const response_json = await response.json()
    console.log(response_json)
    if (!response_json.success) {
        text.value = `An Error Occured: ${response_json}`
        snackbar.value = true
    } else {
        text.value = "Profile Updated Successfully!"
        snackbar.value = true
    }
    
}


</script>

<style scoped>

.container {
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 6rem;
    padding-bottom: 6rem;
}

.filters-form {
    padding-bottom: 3rem;
}

@media (min-width: 100px) {
    .v-form {
        width: 95vw;
    }
}

@media (min-width: 600px) {
    .v-form {
        width: 70vw;
    }
}

@media (min-width: 800px) {
    .v-form {
        width: 50vw;
    }
}

</style>