### Contributors: Lamonte Harris
### Description: Date/Time Helper functions for debugger
from datetime import datetime
import time

import pytz
from dateutil import tz
from pytz import timezone


def create_datetime_hours_list(as_string: bool = False):
    """Used to create a list of hours for drop down list"""
    hours = []
    for val in range(1, 13):
        if as_string:
            hours.append(f"{val}")
        else:
            hours.append(val)
    return hours

def create_datetime_mins_list(step: int = 1, as_string: bool = False):
    """Used to create a list of minutes for drop down list :XX"""
    mins = []
    count = 0

    while count < 60:
        if as_string:
            mins.append(f"{count}")
        else:
            mins.append(count)
        count += step

    return mins


def verify_date(date: str):
    """This function takes a date mm/dd/yyyy formatted date and attempts to verify
    if the date is valid, if it is returns the unix timestamp else returns False"""
    try:
        return time.mktime(datetime.strptime(date, "%m/%d/%Y").timetuple())
    except ValueError:
        return False



def create_course_begin_timestamp(curr_hour: str, curr_min: str, curr_day: str):
    """This function creates a course timestamp that we'll use for every
    course day between the start/end date which we'll create dates using only the hour/min data"""
    plus = 0
    if curr_day == "pm" and curr_hour != "12":
        plus = 12

    if curr_day == "am" and curr_hour == "12":
        curr_hour = "0"

    hour = int(curr_hour) + plus

    today = datetime.today()
    created = datetime(today.year, 1, 1, hour, int(curr_min), 0)

    try:
        return datetime.strptime(f"{created}", "%Y-%m-%d %H:%M:%S").timestamp()
    except ValueError:
        return False


def create_student_timestamp(timestamp: int, curr_hour: str, curr_min: str, curr_day: str):
    """This function creates a course timestamp that we'll use for every
    course day between the start/end date which we'll create dates using only the hour/min data"""
    plus = 0
    if curr_day == "pm" and curr_hour != "12":
        plus = 12

    if curr_day == "am" and curr_hour == "12":
        curr_hour = "0"

    hour = int(curr_hour) + plus
    dt = datetime.fromtimestamp(timestamp)

    created = datetime(dt.year, dt.month, dt.day, hour, int(curr_min), 0)

    try:
        return datetime.strptime(f"{created}", "%Y-%m-%d %H:%M:%S").timestamp()
    except ValueError:
        return False


def convert_timestamp_to_form_begin_mins(timestamp: int, mins: list, double_nums: bool = False):
    """Used to convert the course timestamp data into form data, so we can prefill input minute field"""
    dt = datetime.fromtimestamp(timestamp)
    if dt.minute in mins:
        if double_nums and dt.minute < 10:
            return f"0{dt.minute}"
        return dt.minute
    return None


def convert_timestamp_to_form_begin_hours(timestamp: int):
    """Used to convert the course timestamp data into form data, so we can prefill input hour field"""
    dt = datetime.fromtimestamp(timestamp)
    hour = dt.hour
    if dt.hour == 0:
        hour = 12
    if hour <= 0:
        return 1 # set default value to match form
    if hour > 12:
        hour -= 12
    return hour


def convert_timestamp_to_form_begin_day(timestamp: int):
    """Converts the courses timestamp data and checks if we should show the
    pm or am button depending on if it's before 12pm"""
    dt = datetime.fromtimestamp(timestamp)
    if dt.hour > 11:
        return "pm"
    return "am"


def convert_timestamp_to_form_start_end_date(timestamp: int, return_none: bool = False):
    """used to prefill unix-timestamp data into readable date data"""
    dt = datetime.fromtimestamp(timestamp)
    if timestamp == 0:
        dt = datetime.now()
        if return_none is True:
            return ""

    return dt.strftime("%m/%d/%Y")


def create_student_override_date(timestamp: int):
    """get current datetime if the user override, else return the current time"""
    dt = datetime.fromtimestamp(timestamp)
    dt = dt.replace(tzinfo=pytz.timezone('US/Central'))
    now = datetime.now(pytz.timezone('US/Central'))
    if timestamp == 0:
        dt = now

    hour = dt.hour
    ampm = "am"
    if dt.hour > 12:
        hour = dt.hour - 12

    if dt.hour >= 12:
        ampm = "pm"

    minute = f"{dt.minute}"
    if dt.minute < 10:
        minute = f"0{dt.minute}"

    return "%d/%d/%d %d:%s %s" % (dt.month, dt.day, dt.year, hour, minute, ampm)