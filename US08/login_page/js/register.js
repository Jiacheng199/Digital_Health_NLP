document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();
    //get the registration information from the form
    var username = document.getElementById('reg-username').value;
    var email = document.getElementById('reg-email').value;
    var password = document.getElementById('reg-password').value;
    var confirmPassword = document.getElementById('reg-confirm-password').value;

    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    // Perform registration logic here, e.g., send data to server, validate input, check whether the email is already registered, etc.

    console.log('Username:', username);
    console.log('Email:', email);
    console.log('Password:', password);
});
