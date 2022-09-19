
# import datetime
import pycountry
import unicodedata
from datetime import datetime as dt

import datetime
from datetime import timezone
from datetime import datetime as dt2
# test_string ='1/1/1997'
# #test_string=test_string.replace('-','/')
# new=datetime.datetime.strptime(test_string,'%m/%d/%Y').strftime('%m/%d/%Y')
# print(new)
# test_string.replace('-','/')
# test="2022-09-18 14:27:23"
# test=test.split(" ")
# new=datetime.datetime.strptime(test[0], "%Y-%m-%d").strftime("%m/%d/%Y")
# new=new + " " + test[1]
# print(''.join(new))

test ='uruguay'

test=test.title()
print(test)
# def strip_accents(s):
#    return ''.join(c for c in unicodedata.normalize('NFD', s)
#                   if unicodedata.category(c) != 'Mn')
   
# print(strip_accents('Lucas Hernández'))
#print('2022-09-18T10:27:20Z'[:-1])
# d= dt.fromisoformat('2022-09-18T17:30:20Z'[:-1])
# print(d)
# print(type(d))
# now=datetime.datetime.now().isoformat(sep=' ',timespec="minutes")
# print(type(now))
# m=dt2.strptime(now, '%Y-%m-%d %H:%M')
# print(m-d)
#print(now-d)