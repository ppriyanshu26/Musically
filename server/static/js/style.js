function togglePassword() {
    var passwordInput = document.getElementById('password');
    var eyeIcon = document.getElementById('eyeIcon');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.className = 'fas fa-eye-slash eye-icon';
    } else {
        passwordInput.type = 'password';
        eyeIcon.className = 'fas fa-eye eye-icon';
    }
}

document.getElementById('username').addEventListener('input', function(event) {
    var usernameInput = this.value;
    var label = document.querySelector('.username-label');
    if (!/^[a-zA-Z]*$/.test(usernameInput)) {
        label.classList.add('error');
    } else {
        label.classList.remove('error');
    }
});
