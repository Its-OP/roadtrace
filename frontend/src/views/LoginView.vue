<script setup lang="ts">
  import { ref } from 'vue';
  
  const email = ref('');
  const password = ref('');
  const formHasErrors = true;
  
  const handleSubmit = () => {
    // Handle form submission
    console.log('Email:', email.value);
    console.log('Password:', password.value);
  };
</script>

<template>
  <div class="flex justify-center items-center h-screen bg-gray-100">
    <form @submit.prevent="handleSubmit" class="w-full max-w-sm p-6 bg-white rounded shadow-md relative pb-16">
      <div class="mb-4">
        <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
        <input
            v-model="email"
            type="email"
            id="email"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            required
        />
      </div>
      <div class="mb-6">
        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
        <input
            v-model="password"
            type="password"
            id="password"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            required
        />
      </div>
      <div v-if="formHasErrors" class="mb-4 text-red-500 text-sm font-medium">
        Incorrect email or password
      </div>
      <button
          type="submit"
          class="w-full py-2 px-4 bg-blue-600 text-white font-medium absolute bottom-0 left-0 right-0 rounded-b-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Log In
      </button>
    </form>
  </div>
</template>




<style scoped>

</style>