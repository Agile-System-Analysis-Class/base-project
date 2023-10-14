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

function set_course_start_data(cid) {
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
        console.log(data)
//        if(data.status) {
//            // update access code input on completion
//            showSuccessBlock("Access code updated successfully", 4, function() {
//                window.location = "/teacher/course/" + cid + "/access_code";
//            });
//        } else {
//            showErrorsBlock(data.message, 6);
//        }
    });
}