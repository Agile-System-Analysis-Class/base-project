/* root dashboard functions */
function rootGenerateWebsiteData() {

    $.get("/generate_data", function(data) {
        if(data.status == false) {
            showErrorsBlock(data.message);
        } else {
            // redirect to dashboard
            window.location = "/";
        }
    });

    return false;
}
