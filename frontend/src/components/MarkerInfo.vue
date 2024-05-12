<script setup lang="ts">
  import {Marker} from "../schemas/latLong.ts";
  import {ref, watch} from "vue";

  interface Props {
    marker: Marker | null
  };

  const props = defineProps<Props>();

  const form = ref(null);
  const valid = ref(false);
  const code = ref(props.marker?.source);
  const source = ref(props.marker?.source);
  const initialValues = { code: props.marker?.source, source: props.marker?.source };
  const hasChanges = ref(false);

  const isValidHttpUrl = (string) => {
    let url;

    try {
      url = new URL(string);
    } catch (_) {
      return false;
    }

    return url.protocol === "http:" || url.protocol === "https:";
  }

  const codeRules = [
    v => v.length >= 4 || 'Code must be at least 4 characters',
    v => v.length <= 64 || 'Code must be no more than 64 characters'
  ];
  
  const urlRules = [
    v => isValidHttpUrl(v) || 'Please enter a valid URL'
  ];

  const submitForm = () => {
    if (form.value.validate()) {
      alert('Form is valid!');
    }
  }

  const checkChanges = () => {
    hasChanges.value = code.value !== initialValues.code || source.value !== initialValues.source;
  };

  watch([code, source], checkChanges);
</script>

<template>
  <v-container class="p-0">
    <v-form ref="form" v-model="valid">
      <v-text-field
          v-model="code"
          :rules="codeRules"
          label="Code"
          required
          flat
          solo
          rounded="lg"
          @input="checkChanges"
          bg-color="white"
      ></v-text-field>

      <v-text-field
          v-model="source"
          :rules="urlRules"
          label="Source"
          required
          rounded="lg"
          @input="checkChanges"
          bg-color="white"
      ></v-text-field>

      <v-btn
          v-if="hasChanges && valid"
          @click="submitForm"
      >
        Submit
      </v-btn>
    </v-form>
  </v-container>
</template>

<style>
  .v-field__outline {
    visibility: hidden !important
  }
</style>