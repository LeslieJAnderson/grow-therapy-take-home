import calendar
import datetime

def daterange(start_date, end_date):
    #print(start_date)
    #print(end_date)
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
    yield end_date

def month_range_of(date):
    year = int(date.strftime('%Y'))
    month = int(date.strftime('%m'))

    return {
        'start': datetime.datetime(year, month, 1),
        'end': datetime.datetime(year, month, num_days_in_month(year, month))
    }

def num_days_in_month(year, month):
    monthrange = calendar.monthrange(year, month)
    return monthrange[1]

def week_range_of(date):
    one_week = datetime.timedelta(days=6)
    # turns day into weekly position; sunday into 0, monday into 1, etc.
    day_idx = (date.weekday() + 1) % 7  
    sunday = date - datetime.timedelta(days=day_idx)

    #*LJA_LATER Make note that the beginning of the week isn't always sunday, depending on region. Just show you know that in the documentation.
    return {
        'start': sunday,
        'end': sunday + one_week
    }
