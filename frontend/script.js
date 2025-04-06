document.addEventListener("DOMContentLoaded", function () {
    console.log("Website loaded successfully!");

    const adminUsername = "admin";  // Change as needed
    const adminPassword = "1234";   // Change as needed

    const loginForm = document.getElementById("adminLoginForm");
    const errorMessage = document.getElementById("errorMessage");
    const logoutBtn = document.getElementById("logoutBtn");
    const reviewForm = document.getElementById("reviewForm");
    const reviewList = document.getElementById("reviewList");

    const adminBtn = document.getElementById("adminBtn");
    const userBtn = document.getElementById("userBtn");

    // Welcome page navigation
    if (adminBtn) {
        adminBtn.addEventListener("click", () => {
            window.location.href = "admin-login.html";
        });
    }

    if (userBtn) {
        userBtn.addEventListener("click", () => {
            window.location.href = "user.html";
        });
    }

    // Admin Login
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const enteredUsername = document.getElementById("username").value;
            const enteredPassword = document.getElementById("password").value;

            if (enteredUsername === adminUsername && enteredPassword === adminPassword) {
                localStorage.setItem("isAdmin", "true");
                window.location.href = "admin.html";
            } else {
                errorMessage.textContent = "Invalid username or password!";
            }
        });
    }

    // Admin page access restriction
    if (window.location.pathname.includes("admin.html")) {
        const isAdmin = localStorage.getItem("isAdmin");
        if (isAdmin !== "true") {
            alert("Access Denied! Please log in.");
            window.location.href = "admin-login.html";
        } else {
            fetchReviews();
        }
    }

    // Admin logout
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function () {
            localStorage.removeItem("isAdmin");
            window.location.href = "admin-login.html";
        });
    }

    // Review submission from user.html
    if (reviewForm) {
        reviewForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const name = document.getElementById("name").value;
            const eventName = document.getElementById("event").value;
            const reviewText = document.getElementById("review").value;

            const review = {
                name,
                event: eventName,
                reviewText,
                date: new Date().toISOString()
            };

            fetch("https://backend-dzfe.onrender.com/submit-review", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(review)
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                reviewForm.reset();
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Something went wrong. Please try again later.");
            });
        });
    }

    // Fetch and display reviews on admin.html
    function fetchReviews() {
        fetch("https://backend-dzfe.onrender.com/get-reviews")
            .then(response => response.json())
            .then(data => {
                reviewList.innerHTML = "";
                data.forEach(review => {
                    const li = document.createElement("li");
                    li.textContent = `${new Date(review.date).toLocaleString()} - ${review.name} reviewed "${review.event}": "${review.reviewText}"`;
                    reviewList.appendChild(li);
                });
            })
            .catch(error => {
                console.error("Error fetching reviews:", error);
                reviewList.innerHTML = "<li>Failed to load reviews</li>";
            });
    }
});
