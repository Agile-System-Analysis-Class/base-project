/* login functions */
function attemptLogin() {

    var username = $("#username").siblings("input[name='username']").val().trim();
    var password = $("#password").siblings("input[name='password']").val().trim();

    if(username.length <= 0) {
        showErrorsBlock("Username cannot be left blank");
        return false;
    }

    $.post("/login", {"username": username, "password": password}, function(data) {
        if(data.status == false) {
            showErrorsBlock(data.message);
        } else {
            // redirect to login
            window.location = "/";
        }
    });

    return false;
}


function showErrorsBlock(message, duration = 10) {
    $("#errors-block").html(message).slideDown("slow");
    setTimeout(function(){
        $("#errors-block").slideUp("slow", function() {
            $(this).html("");
        });
    }, duration * 1000);
}