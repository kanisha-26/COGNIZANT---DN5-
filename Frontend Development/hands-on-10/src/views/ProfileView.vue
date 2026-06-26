<template>

<h2>Profile</h2>

<h3>Enrolled Courses</h3>

<ul>

<li

v-for="course in enrolledCourses"

:key="course.id">

{{ course.name }}

</li>

</ul>

<h3>

Total Credits :

{{ totalCredits }}

</h3>

<button

@click="clearAll">

Reset Enrollment

</button>

</template>

<script setup>

import { useEnrollmentStore } from "../stores/enrollment";

import { storeToRefs } from "pinia";

const store = useEnrollmentStore();

const {

enrolledCourses,

totalCredits

} = storeToRefs(store);

function clearAll(){

store.$reset();

}

</script>