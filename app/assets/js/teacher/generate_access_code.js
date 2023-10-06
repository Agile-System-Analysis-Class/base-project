function generate_access_code(cid) {
    $.post("/teacher/course/" + cid + "/access_code", function(data) {
        if(data.status) {
            // update access code input on completion
            showSuccessBlock("Access code updated successfully", 4, function() {
                window.location = "/teacher/course/" + cid + "/access_code";
            });
        } else {
            showErrorsBlock(data.message, 6);
        }
    });
}