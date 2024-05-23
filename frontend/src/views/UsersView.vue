<script setup lang="ts">
  import {computed, reactive, ref, watch} from 'vue';
  import AddUsers from "../components/AddUsers.vue";
  import {User, UserRoles} from "../schemas/latLong.ts";
  const users = ref<User[]>([
    { email: 'user1@example.com', role: 'user' },
    { email: 'user2@example.com', role: 'manager' },
    { email: 'user3@example.com', role: 'administrator' },
  ]);
  
  const originalRoles = reactive(users.value.map(user => user.role));
  const hasChanges = computed(() => {
    return users.value.some(user => user.hasChanged) || users.value.length !== originalRoles.length;
  });

  const saveUsers = () => {
    // Logic to update users
    console.log('Updating users...');
  };
  
  watch(users, (newUsers) => {
    newUsers.forEach((user, index) => {
      user.hasChanged = user.role !== originalRoles[index];
    });
  }, { deep: true });
  
  const deleteUser = (email: string) => {
    users.value = users.value.filter(user => user.email !== email);
  };

  const showAddUserForm = ref(false);

  const handleAddUser = (newUser: User) => {
    users.value.push({ ...newUser, hasChanged: false });
    showAddUserForm.value = false;
  };
</script>

<template>
  <div class="p-5">
    <h1 class="text-xl font-bold mb-4 text-left ml-2">User Management</h1>
    <button
        v-if="hasChanges"
        @click="saveUsers"
        class="bg-blue-500 text-white px-4 py-2 rounded"
    >
      Save
    </button>
    <button
        @click="showAddUserForm = true"
        class="bg-green-500 text-white px-4 py-2 rounded ml-4"
    >
      Add User
    </button>
    <div class="overflow-x-auto bg-white rounded-lg border border-gray-300">
      <table class="min-w-full">
        <thead>
        <tr>
          <th class="py-2 px-4 bg-gray-200 border-b border-gray-300 text-center">Email</th>
          <th class="py-2 px-4 bg-gray-200 border-b border-l border-gray-300 w-40 text-center">Role</th>
          <th class="py-2 px-4 bg-gray-200 border-b border-l border-gray-300 w-32 text-center">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr
            v-for="user in users"
            :key="user.email"
            :class="{ 'bg-orange-200': user.hasChanged }"
            class="border-b border-gray-300"
        >
          <td class="py-2 px-4 border-gray-300">{{ user.email }}</td>
          <td class="py-2 px-4 border-l border-gray-300">
            <select
                v-model="user.role"
                :class="{ 'bg-orange-200': user.hasChanged }"
                class="border rounded px-2 py-1 w-full"
            >
              <option v-for="role in UserRoles" :key="role" :value="role" class="bg-white">{{ role }}</option>
            </select>
          </td>
          <td class="py-2 px-4 border-l border-gray-300">
            <button @click="deleteUser(user.email)" class="bg-red-500 text-white px-4 py-2 rounded w-full">Delete</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
    <AddUsers
      v-if="showAddUserForm"
      @close="showAddUserForm = false"
      @addUser="handleAddUser"
    />
  </div>
</template>

<style>
</style>