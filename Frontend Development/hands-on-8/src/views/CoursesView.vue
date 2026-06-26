<template>
  <div>
    <h2>Course List</h2>

    <input
      type="text"
      placeholder="Search course"
      v-model="searchTerm"
    />

    <hr />

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

      <hr />
    </div>

    <p v-if="filteredCourses.length === 0">
      No courses found.
    </p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import CourseCard from '../components/CourseCard.vue'
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()

const searchTerm = ref('')

const courses = ref([])

onMounted(() => {
  courses.value = [
    {
      id: 1,
      name: 'Java Programming',
      code: 'CS101',
      credits: 4,
      grade: 'A'
    },
    {
      id: 2,
      name: 'Python Programming',
      code: 'CS102',
      credits: 4,
      grade: 'A'
    },
    {
      id: 3,
      name: 'Database Systems',
      code: 'CS103',
      credits: 3,
      grade: 'B+'
    },
    {
      id: 4,
      name: 'Web Development',
      code: 'CS104',
      credits: 4,
      grade: 'A+'
    },
    {
      id: 5,
      name: 'Cloud Computing',
      code: 'CS105',
      credits: 3,
      grade: 'A'
    }
  ]
})

const filteredCourses = computed(() =>
  courses.value.filter(course =>
    course.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
)

function enrollCourse(course) {
  store.enroll(course)
}
</script>

<style scoped>
input {
  padding: 8px;
  width: 250px;
  margin-bottom: 15px;
}

button {
  margin: 10px 0;
  padding: 8px 15px;
  background-color: #42b883;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #369870;
}
</style>