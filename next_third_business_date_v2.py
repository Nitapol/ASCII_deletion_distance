def day_of_week(year, month, day):
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    year -= month < 3
    dw = (year + year // 4 - year // 100 + year // 400 + t[month-1] + day) % 7
    return [6, 0, 1, 2, 3, 4, 5][dw]  # To be consistent with 'datetime' library


def leap_year(year):
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    return True if leap else False


def valid_day(year, month, day):
    month_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year < 1 or year > 9999 or month < 1 or month > 12:
        return False
    m = month_list[month-1] if month != 2 or not leap_year(year) else 29
    return True if 1 <= day <= m else False


class Career(Exception):
        def __str__(self): return 'So I became a waiter...'


MAX_DATE_AND_DAYS_INT = 365 * 100


class Date:
    #         raise ValueError

    def __init__(self, year, month, day):
        if not valid_day(year, month, day):
            raise Career()
        self.y, self.m, self.d = year, month, day

    @classmethod
    def fromstring(cls, s):
        s1, s2, s3 = int(s[0:4]), int(s[4:6]), int(s[6:8])
        return cls(s1, s2, s3)

    def __repr__(self) -> str:
        return '%04d%02d%02d' % (self.y, self.m, self.d)

    def weekday_date(self) -> str:
        names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        return names[self.weekday()] + ' ' + str(self)

    def next_day(self):
        if valid_day(self.y, self.m, self.d + 1):
            return Date(self.y, self.m, self.d + 1)
        elif valid_day(self.y, self.m + 1, 1):
            return Date(self.y, self.m + 1, 1)
        elif valid_day(self.y + 1, 1, 1):
            return Date(self.y + 1, 1, 1)
        else:
            raise Career

    def weekday(self):
        return day_of_week(self.y, self.m, self.d)

    def __add__(self, other):
        "Add a Date to an int."
        if isinstance(other, int):
            if other < 1 or other > MAX_DATE_AND_DAYS_INT:
                raise OverflowError("int > MAX_DATE_AND_DAYS_INT")
            new_date = Date(self.y, self.m, self.d)
            while other >= 1:
                new_date = new_date.next_day()
                other -= 1
            return new_date
        return NotImplemented

    def next_working_day(self):
        day = self.next_day()
        while True:
            while day.weekday() >= 5:
                day = day.next_day()
            holidays_list = year_holidays(day.y)
            for str_day in holidays_list:
                s2 = str(day)
                if str_day == s2:
                    day = day.next_day()
                    break  # for
            if day.weekday() < 5:
                break  # while True
        return day


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
            day = Date(year, h[1], h[2])  # Fixed day
        else:
            day = Date(year, h[1], 1)  # Floating day
            while h[3] != day.weekday():  # Advance to match the weekday
                day = day.next_day()
            count = 1
            while count != h[4]:  # Match the repetition of this day
                next_week = day + 7
                if next_week.m == day.m:
                    day = next_week
                count += 1
        year_list.append(str(day))
    return year_list  # return the holidays as list of strings


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
        today = Date.fromstring(days[0])
        next_day = today.next_working_day()
        third_day = next_day.next_working_day().next_working_day()
        if str(next_day) != days[1] or str(third_day) != days[2]:
            print('*** ERROR *** ', end='')
        else:
            print('              ', end='')
        print(today.weekday_date(), next_day.weekday_date(), third_day.weekday_date())
