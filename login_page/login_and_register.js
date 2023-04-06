document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Perform login logic here, e.g., send data to server, validate user, etc.

    console.log('Username:', username);
    console.log('Password:', password);
});
