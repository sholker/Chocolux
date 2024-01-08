function showHidePass() {
    var x = document.getElementById("password"); // Use the correct id here
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

function toggleUserMenu() {
    var userMenu = document.getElementById("userMenu");
    userMenu.style.display = userMenu.style.display === "block" ? "none" : "block";
}

// Close the user menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.user-icon')) {
        var userMenu = document.getElementById("userMenu");
        if (userMenu.style.display === "block") {
            userMenu.style.display = "none";
        }
    }
}
