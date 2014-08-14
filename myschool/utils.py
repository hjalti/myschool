from datetime import datetime

def parse_date(s):
    return datetime.strptime(s, '%d.%m.%Y %H:%M')

def parse_float(s):
    return float(s.replace(',','.'))

def float_str(f):
    return ('%0.1f'%f).replace('.',',')
