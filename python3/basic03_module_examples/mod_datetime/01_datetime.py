from datetime import date

#// https://docs.python.org/3.6/tutorial/stdlib.html#dates-and-times
#// https://docs.python.org/3.6/library/datetime.html#module-datetime

# dates are easily constructed and formatted
now = date.today()
now   #// now 的类型为 <class 'datetime.date'>
#// datetime.date(2003, 12, 2)

now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B.")
#// '12-02-03. 02 Dec 2003 is a Tuesday on the 02 day of December.'

# dates support calendar arithmetic
birthday = date(1964, 7, 31)
age = now - birthday
age.days
#// 14368










