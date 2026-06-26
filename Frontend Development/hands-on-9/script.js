const cards = document.querySelectorAll(".course-card");
const menuButton = document.getElementById("menuButton");

// Task 129 - Keyboard accessibility
cards.forEach((card) => {

    card.addEventListener("click", () => {
        alert("Course Selected");
    });

    card.addEventListener("keydown", (event) => {

        if (event.key === "Enter") {
            event.preventDefault();
            alert("Course Selected");
        }

    });

});

// Task 131 - Toggle aria-expanded

menuButton.addEventListener("click", () => {

    const expanded = menuButton.getAttribute("aria-expanded");

    if (expanded === "false") {

        menuButton.setAttribute("aria-expanded", "true");

    } else {

        menuButton.setAttribute("aria-expanded", "false");

    }

});