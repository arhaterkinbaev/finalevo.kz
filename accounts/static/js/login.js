document.getElementById("login-form").addEventListener("submit", function(event) {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    if (username === "" || password === "") {
        event.preventDefault(); // Stop form submission
        alert("Please fill in all fields.");
    }
});