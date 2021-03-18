# This module will perform all functions needed for input and reporting dates

import os
import csv
from pathlib import Path
from datetime import date, datetime, timedelta
from rich.console import Console


def change_date(args):  # change date for reports
    current_dir = Path(os.getcwd())
    with open(current_dir / 'reportdate.csv', newline='') as csvfile:
        fieldnames = ['report_date']
        reader = csv.DictReader(csvfile)
        for row in reader:
            report_date = row['report_date']
            if args.now:
                report_date = date.today()
            elif args.yesterday:
                report_date = (date.today() + timedelta(days=-1))
            elif args.date:
                # change date by setting specific date
                report_date = args.date
            elif args.advance_time is not None:
                # change date by advance time (or backwards by negative)
                report_date = (datetime.strptime(report_date, '%Y-%m-%d')
                               .date() + timedelta(days=args.advance_time[0]))
            else:
                continue
            report_date = report_date.strftime('%Y-%m-%d')
            with open(current_dir / 'reportdate.csv', 'w', newline='')\
                 as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'report_date': report_date})

    if args.command is None:
        with open(current_dir / 'reportdate.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                report_date = row['report_date']
                console = Console()
                console.print(f'Changed report date to {report_date}',
                              style='green')


def get_report_date():
    current_dir = Path(os.getcwd())
    with open(current_dir / 'reportdate.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            return row['report_date']


def set_date_range(args):
    # get date from period or reportdate.csv
    if args.month:
        report_date = args.month
    elif args.year:
        report_date = args.year
    else:
        report_date = get_report_date()

    report_date_until = datetime.strptime(report_date, '%Y-%m-%d')
    if args.month:
        report_date_from = report_date_until.replace(day=1)
    elif args.year:
        report_date_from = report_date_until.replace(month=1, day=1)
    else:
        report_date_from = report_date_until
    return report_date_from, report_date_until
