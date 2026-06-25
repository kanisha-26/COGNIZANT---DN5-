import { courses } from "./data.js";

let displayedCourses = [...courses];

const courseGrid = document.querySelector(".course-grid");
const totalCreditsText = document.querySelector("#total-credits");
const searchInput = document.querySelector("#search-courses");
const sortBtn = document.querySelector("#sort-btn");
const selectedCourse = document.querySelector("#selected-course");

function renderCourses(courseList) {

    courseGrid.innerHTML = "";

    courseList.forEach(course => {

        const article = document.createElement("article");

        article.className = "course-card";

        article.dataset.id = course.id;

        article.innerHTML = `
            <h3>${course.name}</h3>
            <p>${course.code}</p>
            <p>${course.credits} Credits</p>
        `;

        courseGrid.appendChild(article);
    });

    const totalCredits =
        courseList.reduce(
            (sum, c) => sum + c.credits,
            0
        );

    totalCreditsText.textContent =
        `Total Credits: ${totalCredits}`;
}

renderCourses(displayedCourses);

searchInput.addEventListener("input", () => {

    const searchText =
        searchInput.value.toLowerCase();

    const filteredCourses =
        courses.filter(course =>
            course.name
                .toLowerCase()
                .includes(searchText)
        );

    displayedCourses = filteredCourses;

    renderCourses(displayedCourses);
});

sortBtn.addEventListener("click", () => {

    displayedCourses.sort(
        (a, b) => b.credits - a.credits
    );

    renderCourses(displayedCourses);
});

courseGrid.addEventListener("click", event => {

    const card =
        event.target.closest(".course-card");

    if (!card) return;

    const selected =
        courses.find(
            c => c.id == card.dataset.id
        );

    selectedCourse.textContent =
        `Selected Course: ${selected.name} | Grade: ${selected.grade}`;
});