async function loadPosts() {

    const loading = document.getElementById("loading");
    const notifications = document.getElementById("notifications");
    const errorMessage = document.getElementById("error-message");
    const retryBtn = document.getElementById("retry-btn");

    loading.style.display = "block";
    notifications.innerHTML = "";
    errorMessage.textContent = "";
    retryBtn.style.display = "none";

    try {

        const response = await fetch(
            "https://jsonplaceholder.typicode.com/posts"
        );

        if (!response.ok) {
            throw new Error("Failed to fetch posts");
        }

        const posts = await response.json();

        loading.style.display = "none";

        posts.slice(0, 5).forEach(post => {

            const card = document.createElement("div");

            card.innerHTML = `
                <h3>${post.title}</h3>
                <p>${post.body}</p>
            `;

            notifications.appendChild(card);
        });

    } catch (error) {

        loading.style.display = "none";

        errorMessage.textContent =
            "Unable to load notifications.";

        retryBtn.style.display = "block";
    }
}

document
    .getElementById("retry-btn")
    .addEventListener("click", loadPosts);

async function fetchUser(id) {

    try {

        const response = await fetch(
            `https://jsonplaceholder.typicode.com/users/${id}`
        );

        const user = await response.json();

        console.log("User:", user.name);

    } catch (error) {

        console.log(error);
    }
}

fetchUser(1);

Promise.all([
    fetch("https://jsonplaceholder.typicode.com/users/1")
        .then(res => res.json()),
    fetch("https://jsonplaceholder.typicode.com/users/2")
        .then(res => res.json())
])
.then(users => {

    console.log(
        "Both Users:",
        users[0].name,
        users[1].name
    );
});

axios.interceptors.request.use(config => {

    console.log(
        "API call started:",
        config.url
    );

    return config;
});

async function loadUserPosts() {

    try {

        const response = await axios.get(
            "https://jsonplaceholder.typicode.com/posts",
            {
                params: {
                    userId: 1
                }
            }
        );

        console.log(
            "Axios Posts:",
            response.data
        );

    } catch (error) {

        console.log(error);
    }
}

loadUserPosts();
loadPosts();

/*
Fetch vs Axios

1. Fetch is built into browsers.
   Axios is an external library.

2. Fetch requires response.json().
   Axios automatically parses JSON.

3. Fetch does not throw errors for 404.
   Axios throws errors automatically.
*/