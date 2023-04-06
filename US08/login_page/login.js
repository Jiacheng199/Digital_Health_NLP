document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    //to to be connected to the backend
    console.log('Username:', username);
    console.log('Password:', password);
});
