import datetime
from datetime import date, timedelta


def day2string(day):
    return '{:%Y%m%d}'.format(day)


def year_holidays(year):
    holidays = [
        ["New Year's Day", 1, 1],  # Fixed: January 1
        ["Birthday of Martin Luther King, Jr.", 1, 0, 0, 3],  # Floating
        ["Washington's Birthday", 2, 0, 0, 3],  # Third Monday in February
        ["Memorial Day", 5, 0, 0, 5],  # Last Monday
        ["Independence Day", 7, 4],
        ["Labor Day", 9, 0, 0, 1],
        ["Columbus Day", 10, 0, 0, 2],
        ["Veterans Day", 11, 11],
        ["Thanksgiving Day", 11, 0, 3, 4],
        ["Christmas Day", 12, 25]
    ]
    year_list = []
    for h in holidays:
        if h[2] > 0:
            day = date(year, h[1], h[2])  # Fixed day
        else:
            day = date(year, h[1], 1)  # Floating day
            while h[3] != day.weekday():  # Advance to match the weekday
                day += timedelta(days=1)
            count = 1
            while count != h[4]:  # Match the repetition of this day
                next_week = day + timedelta(days=7)
                if next_week.month == day.month:
                    day = next_week
                count += 1
        year_list.append(day2string(day))
    return year_list  # return the holidays as list of strings


def str2datetime(string):
    return datetime.datetime.strptime(string, '%Y%m%d')


def next_working_day(string):
    day = str2datetime(string)
    day += timedelta(days=1)
    while True:
        while day.weekday() >= 5:
            day += timedelta(days=1)
        holidays_list = year_holidays(day.year)
        for str_day in holidays_list:
            s2 = day2string(day)
            if str_day == s2:
                day += timedelta(days=1)
                break  # for
        if day.weekday() < 5:
            break  # while True
    return day2string(day)


if __name__ == '__main__':
    dates = [
        ['20190308', '20190311', '20190313'],
        ['20190309', '20190311', '20190313'],
        ['20190310', '20190311', '20190313'],
        ['20190311', '20190312', '20190314'],
        ['20190329', '20190401', '20190403'],
        ['20181231', '20190102', '20190104'],
        ['20190118', '20190122', '20190124'],
        ['20190216', '20190219', '20190221'],
        ['20190526', '20190528', '20190530'],
        ['20190703', '20190705', '20190709'],
        ['20190828', '20190829', '20190903'],
        ['20191010', '20191011', '20191016'],
        ['20191108', '20191112', '20191114'],
        ['20191125', '20191126', '20191129'],
        ['20191224', '20191226', '20191230'],
        ['20191227', '20191230', '20200102']]
    print('\n              Today        Next   and   3rd business day')
    for days in dates:
        next_day = next_working_day(days[0])
        third_day = next_working_day(next_working_day(next_day))
        if next_day != days[1] or third_day != days[2]:
            print('*** ERROR *** ', end='')
        else:
            print('              ', end='')

        def f(x): return datetime.datetime.strftime(str2datetime(x), '%a %x')

        print(f(days[0]), f(next_day), f(third_day))
