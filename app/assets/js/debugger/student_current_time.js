/**
 * Contributors: Lamonte Harris
 * Description: Helper functions for the debugger feature in the professor courses page
 */

/**
 * This function uses the jqueryui for setting up our datepicker
 */
$(function() {
    var dateFormat = "mm/dd/yy",
    curr_date = $( "#current_date" ).datepicker({
            defaultDate: "+1w",
            changeMonth: true,
            numberOfMonths: 3
        });
});

function set_student_current_date(cid) {
    let current_date = $("#current_date").val();
    let set_min = $("#curr_min").val();
    let set_hour = $("#curr_hour").val();
    let set_day = $("#curr_day").val();
    $.post("/student/set_current_time", {
        "current_date": current_date,
        "set_day": set_day,
        "set_min": set_min,
        "set_hour": set_hour,
    }, function(data) {
        if(data.status) {
            // update access code input on completion
            showSuccessBlock("Current student time set successfully!", 2, function() {
                window.location = "/student/course/" + cid;
            });
        } else {
            showErrorsBlock(data.message, 6);
        }
    });
}

function clear_student_current_date(cid) {
    $.post("/student/clear_current_time", function(data) {
        if(data.status) {
            // update access code input on completion
            showSuccessBlock("Current student time reset successfully!", 2, function() {
                window.location = "/student/course/" + cid;
            });
        } else {
            showErrorsBlock(data.message, 6);
        }
    });
}