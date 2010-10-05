import datetime

def _iso_year_start(iso_year):
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta 

def iso_to_datetime(iso_year, iso_week, iso_day=1):
    year_start = _iso_year_start(iso_year)
    return year_start + datetime.timedelta(iso_day-1, 0, 0, 0, 0, 0, iso_week-1)