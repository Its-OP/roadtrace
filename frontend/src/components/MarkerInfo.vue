<script setup lang="ts">
  import {Marker} from "../schemas/latLong.ts";
  import {ref, watch} from "vue";

  interface Props {
    marker: Marker | null,
    onDelete: {
      type: Function,
      required: true
    },
    onUpdate: {
      type: Function,
      required: true
    },
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
    v => !hasChanges.value || v?.length >= 4 || 'Code must be at least 4 characters long',
    v => !hasChanges.value || v?.length <= 64 || 'Code must be no more than 64 characters long'
  ];
  
  const urlRules = [
    v => !hasChanges.value || isValidHttpUrl(v) || 'Please enter a valid URL'
  ];

  const submitForm = () => {
    if (form.value.validate()) {
      props.onUpdate(props.marker?.id, source, code);
      initialValues.value.code = code.value;
      initialValues.value.source = source.value;
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
          @click="_ => onDelete(marker?.id)"
          class="max-w-full w-full rounded-bl rounded-br red--text bg-red-600 delete-btn"
      >
        Delete
      </v-btn>

      <v-btn
          v-if="hasChanges && valid"
          @click="submitForm"
          class="max-w-full w-full rounded-bl rounded-br mt-2"
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
  
  .delete-btn {
    --tw-bg-opacity: 0.8;
    background-color: rgb(220 38 38 / var(--tw-bg-opacity)) !important;
  }
</style>