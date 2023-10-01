function showErrorsBlock(message, duration = 10) {
    $("#errors-block").html(message).slideDown("slow");
    setTimeout(function(){
        $("#errors-block").slideUp("slow", function() {
            $(this).html("");
        });
    }, duration * 1000);
}