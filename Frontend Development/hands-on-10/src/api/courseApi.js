import apiClient from "./apiClient";

export function getAllCourses() {
    return apiClient.get("/users");
}

export function getCourseById(id) {
    return apiClient.get(`/users/${id}`);
}

export function enrollStudent(studentId, courseId) {
    return apiClient.post("/posts", {
        studentId,
        courseId
    });
}