
// pop up login form 
// Select elements
let formBtn = document.querySelector("#login-btn2"); // Button to open form
let loginForm = document.querySelector(".login-form-container"); // Login form container
let formClose = document.querySelector("#form-close"); // Close button

// Ensure the login form is hidden on page load
window.onload = () => {
loginForm.classList.remove("active");
};

// Function to show login form
formBtn.addEventListener("click", () => {
loginForm.classList.add("active"); // Add 'active' class to show form
});

// Function to close login form
formClose.addEventListener("click", () => {
loginForm.classList.remove("active"); // Remove 'active' class to hide form
});

// Close the form when clicking outside of it
window.addEventListener("click", (event) => {
if (event.target === loginForm) {
loginForm.classList.remove("active");
}
});
