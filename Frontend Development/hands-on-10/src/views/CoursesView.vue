<template>
  <div>

    <h2>Course List</h2>

    <input
      type="text"
      placeholder="Search Course"
      v-model="searchTerm"
    />

    <hr>

    <div
      v-for="course in filteredCourses"
      :key="course.id"
    >

      <CourseCard
        :name="course.name"
        :code="course.code"
        :credits="course.credits"
        :grade="course.grade"
      />

      <button @click="enrollCourse(course)">
        Enroll
      </button>

      <hr>

    </div>

    <p v-if="filteredCourses.length===0">
      No Courses Found
    </p>

  </div>
</template>

<script setup>

import { ref, computed, onMounted } from "vue";

import CourseCard from "../components/CourseCard.vue";

import { useEnrollmentStore } from "../stores/enrollment";

import { getAllCourses } from "../api/courseApi";

const store = useEnrollmentStore();

const searchTerm = ref("");

const courses = ref([]);

onMounted(async () => {

    try{

        const data = await getAllCourses();

        courses.value = data.slice(0,5).map((item,index)=>({

            id:index+1,

            name:item.name,

            code:`CS10${index+1}`,

            credits:3,

            grade:"A"

        }));

    }

    catch(error){

        alert(error.message);

    }

});

const filteredCourses = computed(()=>{

    return courses.value.filter(course=>{

        return course.name.toLowerCase().includes(searchTerm.value.toLowerCase());

    });

});

function enrollCourse(course){

    store.enroll(course);

}

</script>

<style scoped>

input{

width:250px;

padding:8px;

margin-bottom:15px;

}

button{

padding:8px 15px;

background:#42b883;

color:white;

border:none;

cursor:pointer;

margin:10px 0;

}

button:hover{

background:#2f9b6d;

}

</style>