/**
 * Contributors: Lamonte Harris
 * Description: Helper functions for the report center
 */

/* handle selecting all/none students from reports page */
function report_center_student_checkboxes() {
    $("#check_all").on("change", function() {
        if($(this).is(":checked")){
            $("input[name='reports[]']").prop("checked", true);
        } else {
            $("input[name='reports[]']").prop("checked", false);
        }
    });
}

/** function to get selected inputs from form to be submitted */
function report_center_get_students_checked_ids() {
    var inputs = [];
    $("input[name='reports[]']").each(function() {
        if($(this).is(":checked")) {
            inputs[inputs.length] = $(this).val();
        }
    });
    return inputs;
}

/** handle students attendance information */
function report_center_generate_student_attendance_report() {
    let students = report_center_get_students_checked_ids();
    if(students.length <= 0) {
        showErrorsBlock("Please select at least one student to view reports on!");
    } else {
        $("#reports-results").html("Loading...");
        $.post("/report-center/results", {"student_ids": JSON.stringify(students)}, function(response) {
            console.log(response);
            if(response.status) {
                $("#reports-results").html(create_report_center_table(response.data));
            } else {
                $("#reports-results").html(create_reports_error(response.message));
            }
        }, "json");
    }
}

/** create html for out attendance reports */
function create_report_center_table(students) {
    let rows = [];
    for(var r = 0; r < students.length; r++) {
        rows[rows.length] = create_reports_center_column(students[r]);
    }
    return `<div class="bg-light mb-4">
            <div class="p-2">
                <h3>Attendance Report Results</h3>
                ${rows.join("")}
            </div>
    </div>`
    return `<div>
        <h3>Attendance Report</h3>
        <table class="table">
            <thead>
            <tr>
                <th scope="col">Student Name</th>
                <th scope="col">Days Attended</th>
                <th scope="col">Days Attended (%)</th>
            </tr>
            </thead>
            <tbody>
            ${rows.join("")}
            </tbody>
        </table>
    </div>`;
}

/** create reports column data */
function create_reports_center_column(student) {
    cols = student.courses.length > 0 ? create_report_center_course_row(student.courses) : [];
    return `<div class="mb-1">
    <div><strong>${student.name}</strong></div>
    <table class="table">
        <thead>
            <tr>
                <th scope="col">Course Name</th>
                <th scope="col">Days Attended</th>
                <th scope="col">Days Attended (%)</th>
                <td scope="col">Overall Attendance</td>
                <td scope="col">Overall Attendance (%)</td>
            </tr>
        </thead>
        <tbody>
            ${cols.join("")}
            <tr>
                <td colspan="3"></td>
                <td>${student.attendance}</td>
                <td>${student.percent}</td>
            </tr>
        </tbody>
    </table>
</div>`;
}

function create_report_center_course_row(courses) {
    let cols = [];
    for(var i = 0; i < courses.length; i++) {
        cols[cols.length] = `<tr>
            <td>${courses[i].name}</td>
            <td>${courses[i].attendance}</td>
            <td>${courses[i].percent}</td>
            <td colspan="2"></td>
        </tr>`;
    }
    return cols;
}

/** reports error block */
function create_reports_error(message) {
    return `<div><h3>Attendance Reports error<h3>
        <div>${message}</div>
    </div>`;
}