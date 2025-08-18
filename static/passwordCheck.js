let password = document.querySelector('input[name="psw"]');
let passwordRepeat = document.querySelector('input[name="psw-repeat"]');
let submitBtn = document.querySelector(".signupbtn");
let username = document.querySelector("input[name='uname']");

// let username = document.querySelector("input[name='uname']");

username.addEventListener("input", function (e) {
    const cursorPosition = this.selectionStart;
    const value = this.value;
    this.value = value.replace(/ /g, "_");

    // Adjust cursor position if it was after a replaced space
    const diff = this.value.length - value.length;
    this.selectionStart = this.selectionEnd = cursorPosition + diff;

    if (this.value.length > 25) {
        this.value = this.value.substring(0, 25);
        this.selectionStart = this.selectionEnd = 25; // Move cursor to end
    }
});

function validateUsername(username) {
    // Regular expression to allow alphanumeric characters and . - _
    const usernameRegex = /^[a-zA-Z0-9._-]{4,25}$/;

    if (usernameRegex.test(username)) {
        return true;
    } else {
        return false;
    }
}

submitBtn.addEventListener("click", (e) => {
    e.preventDefault();
    if (!validateUsername(username.value)) {
        alert(
            "Invalid username, user only alphanumeric characters or . _ - and username must be 4 or more characters long"
        );
    } else if (
        password.value !== passwordRepeat.value ||
        passwordRepeat.value === ""
    ) {
        alert("Passwords do not match or confirmation is empty.");
    } else {
        document.querySelector("form").submit();
    }
});
