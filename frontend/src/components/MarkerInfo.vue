<script setup lang="ts">
  import {Marker} from "../schemas/latLong.ts";
  import {ref, watch} from "vue";

  interface Props {
    marker: Marker | null
  };

  const props = defineProps<Props>();

  const form = ref(null);
  const valid = ref(false);
  const code = ref<string | undefined>(props.marker?.code);
  const source = ref<string | undefined>(props.marker?.source);
  const initialValues = ref({ code: props.marker?.code, source: props.marker?.source });
  const hasChanges = ref(false);

  const checkChanges = () => {
    hasChanges.value = code.value !== initialValues.value.code || source.value !== initialValues.value.source;
  };

  // Watch for changes in the marker prop and update the local state accordingly
  watch(() => props.marker, (newMarker) => {
    if (newMarker) {
      code.value = newMarker.code;
      source.value = newMarker.source;
      initialValues.value = { code: newMarker.code, source: newMarker.source };
      checkChanges();  // Reset the hasChanges state
    }
  }, { immediate: true });

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
    v => v?.length >= 4 || 'Code must be at least 4 characters long',
    v => v?.length <= 64 || 'Code must be no more than 64 characters long'
  ];
  
  const urlRules = [
    v => isValidHttpUrl(v) || 'Please enter a valid URL'
  ];

  const submitForm = () => {
    if (form.value.validate()) {
      alert('Form is valid!');
    }
  }

  watch([code, source], checkChanges);
</script>

<template>
  <div class="bg-white rounded-lg max-w-full w-full p-2">
    <v-form ref="form" v-model="valid">
      <v-text-field
          v-model="code"
          :rules="codeRules"
          label="Code"
          required
          flat
          solo
          rounded="0"
          @input="checkChanges"
      ></v-text-field>

      <v-text-field
          v-model="source"
          :rules="urlRules"
          label="Source"
          required
          rounded="0"
          @input="checkChanges"
      ></v-text-field>

      <v-btn
          v-if="hasChanges && valid"
          @click="submitForm"
          class="max-w-full w-full rounded-bl rounded-br"
      >
        Update
      </v-btn>
    </v-form>
  </div>
</template>

<style>
  .v-field__outline {
    visibility: hidden !important
  }
</style>