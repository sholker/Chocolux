function showHidePass() {
    var x = document.getElementById("password"); // Use the correct id here
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}