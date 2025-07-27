let password = document.querySelector('input[name="psw"]');
let passwordRepeat = document.querySelector('input[name="psw-repeat"]');
let submitBtn = document.querySelector(".signupbtn");

submitBtn.addEventListener('click', (e) => {
    e.preventDefault();

    if (password.value !== passwordRepeat.value || passwordRepeat.value === '') {
        alert("Passwords do not match or confirmation is empty.");
    } else {
        document.querySelector('form').submit();
    }
});
