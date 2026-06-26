<template>
  <header>
    <h1>Student Portal</h1>

    <p>
      Enrolled Courses: {{ store.enrolledCourses.length }}
    </p>
  </header>
</template>

<script setup>
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()
</script>

<style scoped>
header {
  background: #42b883;
  color: white;
  padding: 15px;
  text-align: center;
}
</style>