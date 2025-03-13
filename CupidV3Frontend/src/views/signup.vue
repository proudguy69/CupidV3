<template>
    <div class="container">
        <v-form ref="form" @submit.prevent="submitForm">
            <v-text-field
            label="Name"
            v-model="name"
            :rules="nameRules"
            ></v-text-field>

            <v-select
            label="Age"
            v-model="age"
            :items="ageOptions"
            :rules="selectRules"
            ></v-select>

            <v-text-field
            v-if="age == '26+'"
            label="Age Specified"
            v-model="ageSpecified"
            :rules="ageRules"
            ></v-text-field>

            <v-text-field
            label="Pronouns"
            v-model="pronouns"
            :rules="pronounRules"
            ></v-text-field>

            <v-select
            label="Gender"
            v-model="gender"
            :items="genderOptions"
            :rules="selectRules"
            ></v-select>

            <v-text-field
            v-if="gender=='Other'"
            label="Gender (Specify)"
            v-model="genderSpecified"
            :rules="genderRules"
            ></v-text-field>

            <v-select
            label="Sexuality"
            v-model="sexuality"
            :items="sexualityOptions"
            :rules="selectRules"
            ></v-select>

            <v-textarea
            label="Bio"
            v-model="bio"
            :rules="bioRules"
            ></v-textarea>

            <v-btn class="bg-success" type="submit">Submit</v-btn>
            <v-btn class="bg-error ml-8" @click="deleteProfile">Delete</v-btn>


        </v-form>
        <v-snackbar
        v-model="snackbar"
        :timeout="2000"
        >
        {{ text }}
        </v-snackbar>
    </div>
</template>

<script setup>
import router from '@/router';
import { inject, onMounted, ref } from 'vue';

const userProfile = inject('userProfile')
if (!userProfile.value.username) {
    setTimeout(() => {
        if (!userProfile.value.username) {
            router.push('/')
        } else {
            
        }
    }, 1000)
    router.push('/')
}

const form = ref(null)

const name = ref('')
const age = ref('Select')
const ageSpecified = ref('')
const pronouns = ref('')
const gender = ref('Select')
const genderSpecified = ref('')
const sexuality = ref('Select')
const bio = ref('')

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
}

onMounted(async () => {
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
    })

    const response = await fetch(`/api/profiles/update/${userProfile.value.id}`, {
        method: 'POST',
        headers: {"Content-Type":'application/json'},
        body: data
    })
    const response_json = await response.json()
    if (!response_json.success) {
        text.value = response_json.message
        snackbar.value = true
    } else {
        text.value = "Profile Updated Successfully!"
        snackbar.value = true
    }
    
}


</script>

<style scoped>

.container {
    width: 80vw;
    margin: auto;
    margin-top: 8rem;
}

@media (min-width: 600px) {
    .container {
        width: 65vw;
    }
}

@media (min-width: 800px) {
    .container {
        width: 50vw;
    }
}

</style>