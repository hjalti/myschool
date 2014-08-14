import re
import os

from .utils import parse_float, float_str
from .models import Student

SPLITTER = '----------[Memo]----------'
grade_file_re = re.compile('-?([\d,.]*)-einkunn\.txt', re.I)
students_re = re.compile(r'(\d+) - (.*)')

def get_all_grade_files(d):
    res = []
    for root, dirs, files in os.walk(d):
        for f in files:
            if grade_file_re.match(f):
                res.append(GradeFile(os.path.join(root,f)))
    return res

class GradeFile:
    def __init__(self, file):
        m = grade_file_re.match(os.path.basename(file))
        if m:
            self.grade = parse_float(m.group(1))
        else:
            raise Exception('Not a valid name for a grade file')
        self.file = file
        f = open(file, 'r', encoding='latin1')
        content = f.read()
        f.close()
        try:
            self._header, self.comment = content.split(SPLITTER)
            self.students = [ Student(*(par[::-1])) for par in students_re.findall(self._header) ]
            self.comment = self.comment.strip()
        except Exception as ex:
            print("Error parsing grade file '%s'"%self.file)
            raise ex

    def save(self):
        f = open(self.file, 'w', encoding='latin1')
        f.write(self._header)
        f.write(SPLITTER)
        f.write('\n')
        f.write(self.comment)
        f.close()

        dr, name = os.path.split(self.file)
        os.rename(os.path.join(self.file),os.path.join(dr, '%s-einkunn.txt'%float_str(self.grade)))
