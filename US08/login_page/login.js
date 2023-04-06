document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Connect to the backend here
    console.log('Login - Username:', username);
    console.log('Login - Password:', password);
});

