from datetime import date
from datetime import datetime
d = date.today()
datetime.combine(d, datetime.min.time())

"""
documentation for the strptime command:-

https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

The exif datetime tag has the following format:-
2016:08:17 12:36:08

"""

print("")
print("Working example:-")
datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
print (datetime_object)

datetime_object = datetime.strptime('Feb 1 2005  1:33PM', '%b %d %Y %I:%M%p')
print (datetime_object)


print("")
print("Exif example:-")
datetime_object = datetime.strptime('2016:08:17 12:36:08', '%Y:%m:%d %H:%M:%S')
print (datetime_object)
