import requests as r
import re
from bs4 import BeautifulSoup
import pdb
import urllib.parse
from itertools import groupby
from datetime import datetime

URL = 'https://myschool.ru.is/myschool/'
COURSES = 'https://myschool.ru.is/myschool/?Page=Exe&ID=2.10'
COURSE_ASSIGNMENTS = 'https://myschool.ru.is/myschool/?Page=LMS&ID=16&FagID={0}&View=52&ViewMode=0&Tab=2'
ASSIGNMENT = 'https://myschool.ru.is/myschool/?Page=LMS&ID=16&fagID={0}&View=52&ViewMode=2&Tab=&Act=3&VerkID={1}'
STUDENT_LIST = 'https://myschool.ru.is/myschool/?Page=LMS&ID=8&FagID={0}&View=41&ViewMode=2&Tab=&Filter=0'

COURSE_ID = 'fagid'
ASSIGNMENT_ID = 'verkid'

def parse_qs(url):
    return { k.lower(): v[0]
            for k,v in urllib.parse.parse_qs(url).items() }


class Base:
    def __repr__(self):
        return str(self.__dict__)

class Assignment(Base):
    def __init__(self, name, date, url):
        self.name = name
        self.date = date
        qs = parse_qs(url)
        self.course_id = qs[COURSE_ID]
        self.id = qs[ASSIGNMENT_ID]

class Course(Base):
    def __init__(self, name, url):
        self.id = parse_qs(url)[COURSE_ID]
        self.name, code, _ = name.splitlines()
        self.course_code = re.split('[. ]', code)[1]
        self.semester_code = code.split(',')[0]

class Submission(Base):
    def __init__(self, kt, id, grade, comment):
        self.kt = kt
        self.id = id
        self.grade = grade
        self.comment = comment

class Student(Base):
    def __init__(self, name, username, kt):
        self.name = name
        self.username = username
        self.kt = kt

def get_soup(url, user, passw):
    resp = r.get(url, auth = (user, passw))
    return BeautifulSoup(resp.content)

def parse_date(s):
    return datetime.strptime(s, '%d.%m.%Y %H:%M')

def get_all_courses(user, passw):
    soup = get_soup(COURSES, user, passw)
    return [ Course(tab.span['title'], tab.a['href'])
            for tab in soup.find('ul', class_='ruTabsNew')('li') ]

def get_course_assignments(course_id, user, passw):
    soup = get_soup(COURSE_ASSIGNMENTS.format(course_id), user, passw)
    return [ Assignment(assignment('td')[1].text,
            parse_date(assignment('td')[4].text),
            assignment('td')[1].a['href'])
        for group in soup.find('div', class_='ruContentPage')('table')[1:]
        for assignment in group('tr')[3:-1] ]

def get_assignment_submissions(course_id, assignment_id, user, passw):
    url = ASSIGNMENT.format(course_id, assignment_id)
    soup = get_soup(url, user, passw)
    return list(filter(lambda x: x.id, [ Submission(row('td')[1].text,
                row('td')[3].text.strip(),
                row('td')[7].input['value'],
                row('td')[8].input['value'])
            for row in soup.find('table', class_='ruTable')('tr')[2:-3] ]))

def get_student_list(course_id, user, passw):
    url = STUDENT_LIST.format(course_id)
    soup = get_soup(url, user, passw)
    students = [ Student(row('td')[1].text,
        row('td')[4].text,
        parse_qs(row('td')[5].a['href'])['kt'])
            for row in soup.find('form', id='MyForm')('tr')[1:-2] ]
    return [ next(x) for _, x in groupby(students, lambda x: x.kt) ]


def submit_grades(grades, course_id, assignment_id, user, passw):
    sub_data = {}
    sub_data['Students'] = list(grades.keys())

    for kt, (grade, comment) in grades.items():
        sub_data['grade%s'%kt] = grade
        sub_data['memo%s'%kt] = comment.encode('ISO-8859-1')

    r.post(ASSIGNMENT.format(course_id, assignment_id),
            data=sub_data,
            auth = (user, passw))
