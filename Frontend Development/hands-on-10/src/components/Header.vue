<template>

<header>

<h1>Student Portal</h1>

<p>

Enrolled Courses :

{{ enrolledCourses.length }}

</p>

</header>

</template>

<script setup>

import { useEnrollmentStore } from "../stores/enrollment";

import { storeToRefs } from "pinia";

const store = useEnrollmentStore();

const { enrolledCourses } = storeToRefs(store);

</script>

<style scoped>

header{

background:#1976d2;

color:white;

padding:20px;

text-align:center;

}

</style>