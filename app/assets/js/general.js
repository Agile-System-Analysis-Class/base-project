function showErrorsBlock(message, duration = 6) {
    $("#errors-block").html(message).slideDown("slow");
    setTimeout(function(){
        $("#errors-block").slideUp("slow", function() {
            $(this).html("");
        });
    }, duration * 1000);
}

function showSuccessBlock(message, duration = 6, wait = function(){}) {
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

function hideMessageBlocks() {
    $("#errors-block").slideUp("slow");
    $("#success-block").slideUp("slow");
}

function showWaitingBlock(message, duration = 6, wait = function(){}) {
    $("#waiting-block").html(message).slideDown("slow");
    if(duration == 0) return;
    setTimeout(function(){
        $("#waiting-block").slideUp("slow", function() {
            $(this).html("");
            wait();
        });
    }, duration * 1000);
}