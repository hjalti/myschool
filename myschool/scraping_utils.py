import urllib.parse
import re

from datetime import datetime
from .models import Student, Assignment, Course

COURSE_ID = 'fagid'
ASSIGNMENT_ID = 'verkid'

def parse_date(s):
    return datetime.strptime(s, '%d.%m.%Y %H:%M')

def parse_qs(url):
    return { k.lower(): v[0]
            for k,v in urllib.parse.parse_qs(url).items() }

def parse_assignment_url(url):
    """
    Returns a tuple containing the course ID and the
    assignment ID, respectively.
    """
    qs = parse_qs(url)
    return (qs[COURSE_ID], qs[ASSIGNMENT_ID])

def get_course_id(url):
    return parse_qs(url)[COURSE_ID]

def parse_course_str(full_name):
    name, code, _ = full_name.splitlines()
    course_code = re.split('[. ]', code)[1]
    semester_code = code.split(',')[0]

    return (name, course_code, semester_code)

def create_course(name_str, url):
    return Course(get_course_id(url),
            *parse_course_str(name_str))

def create_assignment(name, date, url):
    cid, id = parse_assignment_url(url)
    return Assignment(id, name, date, cid)


def create_student(name, username, url, group):
    s = Student(name,
        parse_qs(url)['kt'],
        username)
    s.group = group
    return s


