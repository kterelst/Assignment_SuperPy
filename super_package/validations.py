import argparse
import calendar
from datetime import datetime as dt
from decimal import Decimal
from rich.console import Console


def valid_date(date_input):  # check for date-format YYYY-MM-DD
    try:
        date_output = dt.strptime(date_input, '%Y-%m-%d').date()
        return date_output
    except ValueError:
        console = Console()
        console.print("Not a valid date: '{0}'.".format(date_input),
                      style='red')
        exit()


def valid_month(month_input):  # check for date-format YYYY-MM
    try:
        month_output = dt.strptime(month_input, '%Y-%m').date()
        wkday, last_day = calendar.monthrange(
                        int(month_output.strftime('%Y')),
                        int(month_output.strftime('%m')))
        month_last_day = month_input + '-' + str(last_day)
        return month_last_day
    except ValueError:
        console = Console()
        console.print("Not a valid month: '{0}'.".format(month_input),
                      style='red')
        exit()


def valid_year(year_input):  # check for date-format YYYY
    try:
        year_output = dt.strptime(year_input, '%Y').date()
        year_last_day = year_output.replace(month=12, day=31)
        year_last_day = year_last_day.strftime('%Y-%m-%d')
        return year_last_day
    except ValueError:
        console = Console()
        console.print("Not a valid year: '{0}'.".format(year_input),
                      style='red')
        exit()


def valid_float(price_input):  # check for max 2 decimals
    try:
        if Decimal(str(price_input)).as_tuple().exponent >= -2:
            return price_input
        else:  # 3 or more decimals
            msg = "Too many decimals, only 2 allowed: \
                    '{0}'.".format(price_input)
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = "Not a valid price: '{0}'.".format(price_input)
        raise argparse.ArgumentTypeError(msg)
