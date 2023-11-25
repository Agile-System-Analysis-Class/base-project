from app.domain.attendance.attendance_service import get_student_attendance_dates_in_course
from app.domain.clients.clients_repository import find_account_by_id
from app.domain.courses.courses_repository import find_student_courses_by_client_id
from app.domain.courses.courses_service import get_course_dates, get_course_dates_before_or_today


def get_student_attendance_reports_by_ids(ids: list[str]):
    results = []
    for current in ids:
        student = find_account_by_id(int(current))
        if student is None or student.account_type != 3:
            results.append({
                "name": f"id {current} not found",
                "courses": [],
                "attendance": "N/A",
                "percent": "N/A",
            })
            continue

        total_dates_so_far = 0
        total_course_dates_so_far = 0
        total_course_dates = 0

        course_date_results = []

        courses = find_student_courses_by_client_id(student.id)
        for course in courses:
            course_dates = get_course_dates(course)
            course_dates_so_far = get_course_dates_before_or_today(course)
            dates_so_far = get_student_attendance_dates_in_course(student.id, course, course_dates_so_far)

            total_course_dates += len(course_dates)
            total_dates_so_far += len(dates_so_far)
            total_course_dates_so_far += len(course_dates_so_far)

            percent = "NSY"
            if total_course_dates_so_far > 0:
                percent = f"{'%.2f' % ((len(dates_so_far) / len(course_dates_so_far)) * 100)}%"

            course_date_results.append({
                "name": course.course_title,
                "attendance": f"{len(dates_so_far)} / {len(course_dates_so_far)} ({len(course_dates)})",
                "percent": percent,
            })
            #
            # print(course_dates)
            # print(course_dates_so_far)
            # # print(dates)
            # print(dates_so_far)
            # print("----")

        percent = "NSY"
        if total_course_dates_so_far > 0:
            percent = f"{'%.2f' % ((total_dates_so_far / total_course_dates_so_far) * 100)}%"

        results.append({
            "name": f"{student.firstname} {student.lastname} ({student.email})",
            "courses": course_date_results,
            "attendance": f"{total_dates_so_far} / {total_course_dates_so_far} ({total_course_dates})",
            "percent": percent,
        })

    print(results)

    return results