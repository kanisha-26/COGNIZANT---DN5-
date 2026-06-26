<template>
  <div>
    <h2>Course Details</h2>

    <p>Course ID: {{ route.params.id }}</p>

    <button @click="enroll">
      Enroll
    </button>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

function enroll() {
  router.push('/profile')
}
</script>

<style scoped>
button {
  padding: 10px;
}
</style>