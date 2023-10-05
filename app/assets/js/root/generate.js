/* root dashboard functions */
function rootGenerateWebsiteData() {
    showWaitingBlock("Waiting for data to generate", 0);
    $.get("/generate_data", function(data) {
        if(data.status == false) {
            showErrorsBlock(data.message);
        } else {
            // redirect to login
            showSuccessBlock(data.message + ". Now redirecting.", 2, function() {
                window.location = "/";
            });
        }
    });

    return false;
}
