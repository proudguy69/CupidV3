<template>
    <div class="container">
        <v-form>
            <v-text-field
            label="Name"
            v-model="name"
            ></v-text-field>

            <v-text-field
            label="Pronouns"
            v-model="pronouns"
            ></v-text-field>

            <v-select
            label="Gender"
            v-model="gender"
            :items="genderOptions"
            ></v-select>

            <v-text-field
            v-if="gender=='Other'"
            label="Gender (Specify)"
            v-model="genderSpecified"
            ></v-text-field>

            <v-select
            label="Sexuality"
            v-model="sexuality"
            :items="sexualityOptions"
            ></v-select>

            <v-textarea
            label="Bio"
            v-model="bio"
            ></v-textarea>

            <v-btn>Submit</v-btn>


        </v-form>
    </div>
</template>

<script setup>
import { ref } from 'vue';


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