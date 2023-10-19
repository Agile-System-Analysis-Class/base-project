/**
 * Contributors: Lamonte Harris
 * Description: Helper functions for the debugger feature in the professor courses page
 */

/**
 * This function uses the jqueryui for setting up our datepicker
 */
$(function() {
    var dateFormat = "mm/dd/yy",
    from = $( "#start_date" ).datepicker({
            defaultDate: "+1w",
            changeMonth: true,
            numberOfMonths: 3
        }).on( "change", function() {
        console.log("changed");
            $("#end_date").datepicker( "option", "minDate", getDate( this ) );
        }),
    to = $( "#end_date" ).datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 3
    });

    /* Helper function used to parse date */
    function getDate( element ) {
      var date;
      try {
        date = $.datepicker.parseDate( dateFormat, element.value );
      } catch( error ) {
        date = null;
      }
      return date;
    }
});

function set_course_start_data(cid) {
    let start_date = $("#start_date").val();
    let end_date = $("#end_date").val();
    let set_min = $("#begin_min").val();
    let set_hour = $("#begin_hour").val();
    let set_day = $("#begin_day").val();
    $.post("/teacher/course_set_data/" + cid, {
        "start_date": start_date,
        "end_date": end_date,
        "set_day": set_day,
        "set_min": set_min,
        "set_hour": set_hour,
    }, function(data) {
        console.log(data)
        if(data.status) {
            // update access code input on completion
            showSuccessBlock("Course data updated successfully!", 4, function() {
                hideMessageBlocks();
            });
        } else {
            showErrorsBlock(data.message, 6);
        }
    });
}