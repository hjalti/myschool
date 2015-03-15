import requests as r
import pdb

from bs4 import BeautifulSoup
from itertools import groupby
from .scraping_utils import parse_date, create_course, create_student, create_assignment, create_submission
from .models import Submission
from .utils import float_str, parse_float

URL = 'https://myschool.ru.is/myschool/'
COURSES = 'https://myschool.ru.is/myschool/?Page=Exe&ID=2.10'
COURSE_ASSIGNMENTS = 'https://myschool.ru.is/myschool/?Page=LMS&ID=16&FagID={0}&View=52&ViewMode=0&Tab=2'
ASSIGNMENT = 'https://myschool.ru.is/myschool/?Page=LMS&ID=16&fagID={0}&View=52&ViewMode=2&Tab=&Act=3&VerkID={1}'
STUDENT_LIST = 'https://myschool.ru.is/myschool/?Page=LMS&ID=8&FagID={0}&View=41&ViewMode=2&Tab=&Filter=0'


def get_soup(url, user, passw):
    resp = r.get(url, auth = (user, passw))
    return BeautifulSoup(resp.content)

def get_all_courses(user, passw):
    soup = get_soup(COURSES, user, passw)
    return [ create_course(tab.span['title'], tab.a['href'])
            for tab in soup.find('ul', class_='ruTabsNew')('li') ]

def get_course_assignments(course_id, user, passw):
    soup = get_soup(COURSE_ASSIGNMENTS.format(course_id), user, passw)
    return [ create_assignment(assignment('td')[1].text,
            parse_date(assignment('td')[4].text),
            assignment('td')[1].a['href'])
        for group in soup.find('div', class_='ruContentPage')('tbody')
        for assignment in group('tr')[1:-1] ]

def get_assignment_submissions(course_id, assignment_id, user, passw):
    url = ASSIGNMENT.format(course_id, assignment_id)
    soup = get_soup(url, user, passw)
    return list(filter(lambda x: x.id, [ create_submission(row('td')[1].text,
                row('td')[3].text.strip(),
                row('td')[7].input['value'],
                row('td')[8].input['value'])
            for row in soup.find('table', class_='ruTable')('tr')[2:-3] ]))

def get_student_list(course_id, user, passw):
    url = STUDENT_LIST.format(course_id)
    soup = get_soup(url, user, passw)
    students = [ create_student(row('td')[1].text,
        row('td')[4].text,
        row('td')[5].a['href'],
        row('td')[6].text)
            for row in soup.find('form', id='MyForm')('tr')[1:-2] ]
    return [ next(x) for _, x in groupby(students, lambda x: x.kt) ]


def submit_grades(submissions, course_id, assignment_id, user, passw):
    sub_data = {}
    sub_data['Students'] = list(map(lambda x: x.kt, submissions))

    for sub in submissions:
        sub_data['grade%s'%sub.kt] = float_str(sub.grade)
        sub_data['memo%s'%sub.kt] = sub.comment.encode('ISO-8859-1')

    r.post(ASSIGNMENT.format(course_id, assignment_id),
            data=sub_data,
            auth = (user, passw))
