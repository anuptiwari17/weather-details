// Add interactivity for error messages or animations
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const errorMessage = document.querySelector("p[style*='color: red;']");

    // Auto-hide error message after 5 seconds
    if (errorMessage) {
        setTimeout(() => {
            errorMessage.style.display = "none";
        }, 5000);
    }

    // Add animations for form submission
    form.addEventListener("submit", () => {
        form.style.opacity = "0.5";
        setTimeout(() => {
            form.style.opacity = "1";
        }, 500);
    });
});




