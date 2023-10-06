import datetime
import calendar
import schedule
import time

weekday = calendar.weekday(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)

cl = calendar.LocaleTextCalendar(firstweekday=0, locale=('Russian_Russia', '1251'))
# print(cl.formatmonth(2023, 9).split("\n")[0])

weekdays = cl.formatmonth(2023, 9).split("\n")[1].split(" ")
# print(weekdays)


def job():
    return print("Сработало!")


print(callable(job))

schedule.every(1).minutes.do(job_func=job)

while True:
    schedule.run_pending()
    time.sleep(1)

