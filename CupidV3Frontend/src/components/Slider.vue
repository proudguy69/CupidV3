<template>
    <v-range-slider
    v-model="age_model"
    :max="max"
    :min="min"
    :step="1"
    class="align center"
    >

    <template v-slot:prepend>
        <v-text-field
        v-model="age_model[0]"
        density="compact"
        style="width: 70px"
        type="number"
        variant="outlined"
        hide-details
        single-line
        >
        </v-text-field>
    </template>

    <template v-slot:append>
        <v-text-field
        v-model="age_model[1]"
        density="compact"
        style="width: 70px"
        type="number"
        variant="outlined"
        hide-details
        single-line
        >
        </v-text-field>
    </template>

    </v-range-slider>
</template>

<script setup>
import { ref, toRef, watch } from 'vue';
const age_model = defineModel()

const min = ref(13)
const max = ref(18)



if (age_model.value[0]+2 >= 18) {
    min.value = 18
    max.value = 50
}

watch(age_model, (_) => {
    if (age_model.value[0]+2 >= 18) {
        min.value = 18
        max.value = 50
    }
}, {deep:true})

</script>