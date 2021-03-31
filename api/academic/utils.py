from django.core.validators import MaxValueValidator
import datetime


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def min_max_year():
    year_today = datetime.date.today().year
    year_initial = 2000
    return list_years(year_initial, year_today)


def list_years(year_initial, year_today):
    years = list()

    for x in range(year_today-(year_initial-1)):
        years.append({'id': x, 'year': year_initial+x})

    return years
