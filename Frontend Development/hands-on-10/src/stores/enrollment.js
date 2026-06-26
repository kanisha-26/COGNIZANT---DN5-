import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { getCourseById } from "../api/courseApi";

export const useEnrollmentStore = defineStore("enrollment", () => {

    const enrolledCourses = ref([]);

    const totalCredits = computed(() => {

        return enrolledCourses.value.length * 3;

    });

    function enroll(course) {

        enrolledCourses.value.push(course);

    }

    function unenroll(courseId) {

        enrolledCourses.value =
            enrolledCourses.value.filter(c => c.id !== courseId);

    }

    async function fetchAndEnroll(courseId) {

        const course = await getCourseById(courseId);

        enrolledCourses.value.push(course);

    }

    function $reset() {

        enrolledCourses.value = [];

    }

    return {

        enrolledCourses,

        totalCredits,

        enroll,

        unenroll,

        fetchAndEnroll,

        $reset

    };

});