from getpass import getpass

from myschool.models import Submission
from myschool.api import submit_grades

# You need to extract the course ID and the assignment ID from the URL of the assignment

COURSE_ID = 1337    #fagID in URL
ASSGN_ID = 7331     #verkID in URl

# Create a list of grades and comments to submit

# Submission constructor takes 4 arguments
# 1: The kennitala of the student
# 2: The ID of the submission, should be None if you are submitting grades
# 3: The grade given to the assignment
# 4: The comment given to the assignment

subs = [ Submission('0123456789', None, 9.3, 'A comment'),
        Submission('0123456799', None, 3.3, 'Another comment') ]

# Submits grades to myschool.
# NOTE: Grades need to be published manually on MySchool or you can call
# the post_grades function in the api.
submit_grades(subs, COURSE_ID, ASSGN_ID, input('Username: '), getpass())


