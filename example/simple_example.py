from getpass import getpass

from myschool.models import Submission
from myschool.api import submit_grades

COURSE_ID = 1337
ASSGN_ID = 7331

subs = [ Submission('0123456789', None, 9.3, 'A comment'),
        Submission('0123456799', None, 3.3, 'Another comment') ]

submit_grades(COURSE_ID, ASSGN_ID, input('Username: '), getpass())


