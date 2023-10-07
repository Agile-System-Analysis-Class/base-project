function showErrorsBlock(message, duration = 10) {
    $("#errors-block").html(message).slideDown("slow");
    setTimeout(function(){
        $("#errors-block").slideUp("slow", function() {
            $(this).html("");
        });
    }, duration * 1000);
}

function showSuccessBlock(message, duration = 10, wait = function(){}) {
    $("#errors-block").hide();
    $("#waiting-block").hide();
    $("#success-block").html(message).slideDown("slow");
    setTimeout(function(){
        $("#success-block").slideUp("slow", function() {
            $(this).html("");
            wait();
        });
    }, duration * 1000);
}

function showWaitingBlock(message, duration = 10, wait = function(){}) {
    $("#waiting-block").html(message).slideDown("slow");
    if(duration == 0) return;
    setTimeout(function(){
        $("#waiting-block").slideUp("slow", function() {
            $(this).html("");
            wait();
        });
    }, duration * 1000);
}