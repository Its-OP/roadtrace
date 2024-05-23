<script setup lang="ts">
  import { ref } from 'vue';
  import {User, UserRoles} from "../schemas/latLong.ts";

  const emit = defineEmits(['close', 'addUser']);
  
  const formData = ref<User>({
    email: '',
    password: '',
    role: UserRoles[0],
  });

  const addUser = () => {
    emit('addUser', formData.value);
    closeForm();
  };

  const closeForm = () => {
    emit('close');
  };
</script>


<template>
  <div class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-96">
      <h2 class="text-xl font-bold mb-4">Add New User</h2>
      <form @submit.prevent="addUser">
        <div class="mb-4">
          <label for="email" class="block text-gray-700 mb-2">Email</label>
          <input
              v-model="formData.email"
              type="email"
              id="email"
              class="border rounded px-3 py-2 w-full"
              required
          />
        </div>
        <div class="mb-4">
          <label for="password" class="block text-gray-700 mb-2">Password</label>
          <input
              v-model="formData.password"
              type="password"
              id="password"
              class="border rounded px-3 py-2 w-full"
              required
          />
        </div>
        <div class="mb-4">
          <label for="role" class="block text-gray-700 mb-2">Role</label>
          <select
              v-model="formData.role"
              id="role"
              class="border rounded px-3 py-2 w-full"
              required
          >
            <option v-for="role in UserRoles" :key="role" :value="role">{{ role }}</option>
          </select>
        </div>
        <div class="flex justify-end">
          <button type="button" @click="closeForm" class="bg-gray-500 text-white px-4 py-2 rounded mr-2">Cancel</button>
          <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">Add</button>
        </div>
      </form>
    </div>
  </div>
</template>


<style scoped>

</style>