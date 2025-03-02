<template>
    <div class="container">
        <v-form ref="form" @submit.prevent="submitForm">
            <v-text-field
            label="Name"
            v-model="name"
            :rules="nameRules"
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


        </v-form>
    </div>
</template>

<script setup>
import { inject, ref } from 'vue';

const user_data = inject('user_data')

const form = ref(null)

const name = ref('')
const pronouns = ref('')
const gender = ref('Select')
const genderSpecified = ref('')
const sexuality = ref('Select')
const bio = ref('')

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


const nameRules = ref([
    function characterLimit(value) {
        if (value.length >=3 && value.length <= 20) return true
        return 'Name must be between 3 and 20 characters'
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




async function submitForm() {
    await form.value.validate()
    if (!form.value.isValid) {return}
    const data = JSON.stringify({
        user_id:user_data.value.id,
        name:name.value,
        pronouns:pronouns.value,
        gender:gender.value,
        gender_specified:genderSpecified.value,
        sexuality:sexuality.value,
        bio:bio.value,
    })

    const response = await fetch('/api/update/profile', {
        method: 'POST',
        headers: {"Content-Type":'application/json'},
        body: data
    })
    const response_json = await response.json()
    console.log(response_json)
    
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