function attend_course(cid) {
    let access_code = $("#access_code").val();
    $.post("/student/course/" + cid + "/attendance", {
        "access_code": access_code,
    }, function(data) {
        if(data.status) {
            // update access code input on completion
            showSuccessBlock("You self-checked into your course successfully!", 2, function() {
                window.location = "/student/course/" + cid;
            });
        } else {
            showErrorsBlock(data.message, 6);
        }
    });
}