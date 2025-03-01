<template>
  <v-container>
    <v-card class="mx-auto pa-4">
      <v-card-title>Create Your Profile</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submitProfile">
          <v-text-field 
            v-model="profile.name" 
            label="Name" 
            required 
            outlined
          ></v-text-field>

          <v-select 
            v-model="profile.pronouns" 
            :items="pronounsOptions" 
            label="Pronouns" 
            outlined 
            required
          ></v-select>

          <v-select 
            v-model="profile.gender" 
            :items="genderOptions" 
            label="Gender" 
            outlined
          ></v-select>

          <v-textarea 
            v-model="profile.bio" 
            label="Bio" 
            rows="3" 
            outlined
          ></v-textarea>

          <v-text-field 
            v-model="profile.height" 
            label="Height (cm)" 
            type="number" 
            outlined
          ></v-text-field>

          <v-file-input 
            v-model="profile.image" 
            label="Profile Image" 
            accept="image/*" 
            outlined
          ></v-file-input>

          <v-btn type="submit" color="primary" class="mt-3" block>
            Save Profile
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';

const profile = ref({
  name: '',
  pronouns: '',
  gender: '',
  bio: '',
  height: '',
  image: null
});

const pronounsOptions = ['He/Him', 'She/Her', 'They/Them', 'Other'];
const genderOptions = ['Male', 'Female', 'Non-Binary', 'Other'];

const submitProfile = () => {
  console.log('Profile submitted:', profile.value);
  // Send to API
};
</script>

<style scoped>
.v-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
</style>
