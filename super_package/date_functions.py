# This module will perform all functions needed for input and reporting dates

import os
import csv
from datetime import date, datetime, timedelta


def change_date(args):  # change date for reports
    with open(os.getcwd()+'\\reportdate.csv', newline='') as csvfile:
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
            with open(os.getcwd()+'\\reportdate.csv', 'w', newline='')\
                 as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'report_date': report_date})


def get_report_date():
    with open(os.getcwd()+'\\reportdate.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            return row['report_date']
