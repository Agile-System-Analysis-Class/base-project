

/* handle selecting all/none students from reports page */
function reports_student_checkboxes() {
    $("#check_all").on("change", function() {
        if($(this).is(":checked")){
            $("input[name='reports[]']").prop("checked", true);
        } else {
            $("input[name='reports[]']").prop("checked", false);
        }
    });
}

/** function to get selected inputs from form to be submitted */
function reports_get_students_checked_ids() {
    var inputs = [];
    $("input[name='reports[]']").each(function() {
        if($(this).is(":checked")) {
            inputs[inputs.length] = $(this).val();
        }
    });
    return inputs;
}

/** handle students attendance information */
function reports_generate_student_attendance_report(cid) {
    let students = reports_get_students_checked_ids();
    if(students.length <= 0) {
        $("#reports-results").html(create_reports_error("Please select at least one student to generate a report on!"));
    } else {
        $("#reports-results").html("Loading...");
        $.post("/teacher/course/generate_report/" + cid, {"student_ids": JSON.stringify(students)}, function(data) {
            if(data.status) {
                $("#reports-results").html(create_reports_table("", data.data));
            } else {
                $("#reports-results").html(create_reports_error(data.message));
            }
        }, "json");
    }
}

/** create html for out attendance reports */
function create_reports_table(title, results) {
    let rows = [];
    for(var r = 0; r < results.length; r++) {
        rows[rows.length] = create_reports_column(results[r].student.name, results[r].attendance, results[r].attendance_percent);
    }
    return `<div>
        <h3>Attendance Report</h3>
        <table border="1px">
            <tr>
                <th>Student Name</th>
                <th>Days Attended</th>
                <th>Days Attended (%)</th>
            </tr>
            ${rows.join("")}
        </table>
    </div>`;
}

/** create reports column data */
function create_reports_column(name, attendance, percentage) {
    console.log(name, attendance, percentage)
    return `<tr>
            <td>${name}</td>
            <td align="center">${attendance}</td>
            <td>${percentage} Attendance</td>
        </tr>`;
}

/** reports error block */
function create_reports_error(message) {
    return `<div><h3>Attendance Reporting error<h3>
        <div>${message}</div>
    </div>`;
}