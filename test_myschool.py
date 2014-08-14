import myschool as m
from getpass import getpass

auth = (input('Username: '), getpass())

x1 = m.get_all_courses(*auth)

assert(x1)

x2 = m.get_course_assignments('25124', *auth)

x3 = m.get_assignment_submissions('25124','43544', *auth)

x4 = m.get_student_list('25124', *auth)

#p = get_soup(STUDENT_LIST.format('25124'), *auth)
