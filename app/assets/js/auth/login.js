/* Contributors: Lamonte */

/* login functions */
function attemptLogin() {

    var email = $("#email").siblings("input[name='email']").val().trim();
    var password = $("#password").siblings("input[name='password']").val().trim();
    console.log("pressed");
    if(email.length <= 0) {
        showErrorsBlock("Email/Username cannot be left blank");
        return false;
    }
    if(password.length <= 0) {
        showErrorsBlock("Password cannot be left blank");
        return false;
    }

    $.post("/login", {"email": email, "password": password}, function(data) {
        if(data.status == false) {
            showErrorsBlock(data.message);
        } else {
            // redirect to login
            showSuccessBlock("Login successful", 2, function() {
                window.location = "/";
            });
        }
    });

    return false;
}