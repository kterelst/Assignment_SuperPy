# Program for recording buy and sale and reporting them

import argparse
import csv
import os
import calendar
import super_package
from datetime import date
from datetime import datetime as dt
from decimal import Decimal
from rich.console import Console

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'


# Your code below this line.
def main():

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

    def find_bought_id(args, sold_id):  # find same product not sold
        try:
            bought_id = None
            with open(os.getcwd()+'\\bought.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                reader_list = []
                reader_list.extend(reader)
                for row in reader_list:  # FIFO, if LIFO: reversed(reader_list)
                    # find line: not sold, same product
                    if not row['sold_id'] and (row['product_name'] ==
                                               args.product_name):
                        bought_id = int(row['id'])
                        row['sold_id'] = sold_id
                        break
                    else:
                        continue
                # rewrite bought.csv with updated sold-field
                fieldnames = ['id', 'product_name', 'buy_date', 'buy_price',
                              'expiration_date', 'sold_id']
                with open(os.getcwd()+'\\bought.csv', 'w', newline='')\
                     as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(reader_list)
            return bought_id
        except OSError:
            return None

    # general
    parser = argparse.ArgumentParser(
             description='supermarket inventory: current, IN and out')
    subparsers = parser.add_subparsers(title='commands',
                                       dest='command',
                                       help='sub-command help')

    date_group = parser.add_argument_group()
    date_input_group = date_group.add_mutually_exclusive_group()
    date_input_group.add_argument('--now', '--today',
                                  action='store_true',
                                  help='Set date to today for reports')
    date_input_group.add_argument('--yesterday',
                                  action='store_true',
                                  help='Set date to yesterday for reports')
    date_input_group.add_argument('--date',
                                  type=valid_date,
                                  help='Set specific date for reports',
                                  metavar='yyyy-mm-dd')
    date_input_group.add_argument('--advance-time',
                                  type=int,
                                  nargs=1,
                                  help='Number of days forward or backwards\
                                  from last command',
                                  metavar='N')

    # buy and sell commands
    buy_sell = argparse.ArgumentParser(add_help=False)
    buy_sell.add_argument('--product-name',
                          required=True,
                          help='The product name')
    buy_sell.add_argument('--price',
                          type=valid_float,
                          required=True,
                          help='The price rounded to 2 decimals',
                          metavar='9.99')

    buy_group = subparsers.add_parser('buy',
                                      parents=[buy_sell],
                                      help='Put product in inventory\
                                           (You\'ve bought it)')
    buy_group.add_argument('--expiration-date',
                           type=valid_date,
                           default=9999-12-31,
                           help='The expiration date',
                           metavar='yyyy-mm-dd')

    sell_group = subparsers.add_parser('sell',
                                       parents=[buy_sell],
                                       help='Remove product from inventory\
                                            (You\'ve sold it)')

    # reports commands
    reports = ['inventory', 'revenue', 'profit', 'buy', 'sell']
    report_group = subparsers.add_parser('report',
                                         help='Display report')
    report_group.add_argument('type',
                              nargs='?',
                              choices=reports,
                              help='Available reports are: '+', '
                                   .join(reports),
                              metavar=''+', '.join(reports))
    report_group.add_argument('-e', '--excel',
                              action='store_true',
                              help='Export to Excel')
    report_group.add_argument('-c', '--csv',
                              action='store_true',
                              help='Export to CSV')

    # howto impove? repeating! add parent not possible because -h conflict
    report_date_group = report_group.add_mutually_exclusive_group()
    report_date_group.add_argument('--now', '--today',
                                   action='store_true',
                                   help='Set date to today for reports')
    report_date_group.add_argument('--yesterday',
                                   action='store_true',
                                   help='Set date to yesterday for reports')
    report_date_group.add_argument('--date',
                                   type=valid_date,
                                   help='Set specific date for reports',
                                   metavar='yyyy-mm-dd')
    report_date_group.add_argument('--month',
                                   type=valid_month,
                                   help='Use specific month for report',
                                   metavar='yyyy-mm')
    report_date_group.add_argument('--year',
                                   type=valid_year,
                                   help='Use specific year for report',
                                   metavar='yyyy')
    report_date_group.add_argument('--advance-time',
                                   type=int,
                                   nargs=1,
                                   help='Number of days forward or backwards\
                                        from last setting',
                                   metavar='N')

    # general
    args = parser.parse_args()
    # print(args)

    # start of processing commands
    console = Console()

    # change date setting for reports
    if args.now or args.yesterday or args.date or args.advance_time:
        super_package.change_date(args)
        if args.command is None:
            with open(os.getcwd()+'\\reportdate.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    report_date = row['report_date']
                    console.print(f'Changed report date to {report_date}',
                                  style='green')

    # increase id-number for buy/sell
    if args.command == 'buy' or args.command == 'sell':
        try:
            fieldnames = ['bought_id', 'sold_id']
            with open(os.getcwd()+'\\id.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # increase current id-number by 1
                    if args.command == 'buy':
                        bought_id = int(row['bought_id'])
                        bought_id += 1
                        row['bought_id'] = bought_id
                    elif args.command == 'sell':
                        sold_id = int(row['sold_id'])
                        sold_id += 1
                        row['sold_id'] = sold_id
                    else:
                        continue
                    # rewrite id.csv with updated id-number for every buy/sell
                    with open(os.getcwd()+'\\id.csv', 'w', newline='')\
                         as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow(row)
        except OSError:
            console.print('Failed updating id.csv', style='red')
            return

    if args.command == 'buy':
        try:
            fieldnames = ['id',
                          'product_name',
                          'buy_date',
                          'buy_price',
                          'expiration_date',
                          'sold_id']
            line = {'id': bought_id,
                    'product_name': args.product_name,
                    'buy_date': date.today(),
                    'buy_price': args.price,
                    'expiration_date': args.expiration_date,
                    'sold_id': None}
            with open(os.getcwd()+'\\bought.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(line)
            console.print('Recorded', style='green')
        except OSError:
            console.print('NOT recorded in bought.csv', style="red")

    elif args.command == 'sell':
        try:
            bought_id_corresponding = find_bought_id(args, sold_id)
            if bought_id_corresponding:
                fieldnames = ['id',
                              'product_name',
                              'sell_date',
                              'sell_price',
                              'bought_id']
                line = {'id': sold_id,
                        'product_name': args.product_name,
                        'sell_date': date.today(),
                        'sell_price': args.price,
                        'bought_id': bought_id_corresponding}
                with open(os.getcwd()+'\\sold.csv', 'a', newline='')\
                     as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow(line)
                console.print('Recorded', style='green')
            else:
                console.print('Product not in stock', style='red')
        except OSError:
            console.print('NOT recorded in sold.csv', style='red')

    elif args.command == 'report':

        # get date from period or reportdate.csv
        if args.month:
            report_date = args.month
        elif args.year:
            report_date = args.year
        else:
            report_date = super_package.get_report_date()

        if args.type == 'sell':  # not implemented (yet): date-specific
            super_package.print_report('sold.csv', 'Sold', args)

        elif args.type == 'buy':  # not implemented (yet): date-specific
            super_package.print_report('bought.csv', 'Bought', args)

        elif args.type == 'inventory':
            try:
                bought_id = None
                # check for same prod; write count in tmpinventory.csv
                with open(os.getcwd()+'\\bought.csv', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    reader_list_new = []
                    done_list = []
                    reader_list = []
                    reader_list.extend(reader)
                    for row in reader_list:
                        if row['id'] in done_list:
                            next
                        else:
                            new_row = row.copy()
                            count = 0
                            for row in reader_list:
                                if row['id'] in done_list:
                                    next
                                else:
                                    check_date = dt.strptime(report_date,
                                                             '%Y-%m-%d')
                                    # if bought after report_date: skip
                                    if dt.strptime(row['buy_date'],
                                                   '%Y-%m-%d') > check_date:
                                        done_list.append(row['id'])

                                    # if expired: skip
                                    elif dt.strptime(row['expiration_date'],
                                                     '%Y-%m-%d') < check_date:
                                        done_list.append(row['id'])
                                    else:
                                        # if sold before report_date: skip
                                        if row['sold_id']:
                                            with open(os.getcwd()+'\\sold.csv',
                                                 newline='') as csvfile:
                                                reader_sold = csv.DictReader(
                                                              csvfile)
                                                for row_sold in reader_sold:
                                                    if (row_sold['id'] ==
                                                       row['sold_id']):
                                                        if (dt.strptime(
                                                           row_sold
                                                           ['sell_date'],
                                                           '%Y-%m-%d')
                                                           <= check_date):
                                                            done_list.append(
                                                                      row['id']
                                                                      )

                                if row['id'] not in done_list:
                                    # if same product, price and exp.date: add
                                    if (row['product_name'] ==
                                       new_row['product_name'] and
                                       row['buy_price'] ==
                                       new_row['buy_price'] and
                                       row['expiration_date'] ==
                                       new_row['expiration_date']):
                                        count += 1
                                        done_list.append(row['id'])

                            # write to reader_list_new if item in inventory
                            if count:
                                del new_row['id']
                                del new_row['buy_date']
                                del new_row['sold_id']
                                new_row['count'] = count
                                reader_list_new.append(new_row)

                    # write tmpinventory.csv with count of same article
                    fieldnames = ['product_name',
                                  'count',
                                  'buy_price',
                                  'expiration_date']
                    with open(os.getcwd() + '\\tmpinventory.csv', 'w',
                              newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(reader_list_new)

                title = 'Inventory' + '_' + str(report_date)
                super_package.print_report('tmpinventory.csv', title, args)

            except OSError:
                console.print('Not able to report inventory', style='red')
                return

            # remove tmpinventory.csv after use
            try:
                os.remove(os.getcwd()+'\\tmpinventory.csv')
            except OSError:
                pass

        elif args.type == 'revenue':
            report_date_until = dt.strptime(report_date, '%Y-%m-%d')
            if args.month:
                report_date_from = report_date_until.replace(day=1)
            elif args.year:
                report_date_from = report_date_until.replace(month=1, day=1)
            else:
                report_date_from = report_date_until

            try:
                if report_date_from > dt.today():
                    if args.month or args.year:
                        console.print(f'No revenue for [bold]future[/bold]\
                                      date-range {report_date_from.date()}\
                                      until {report_date_until.date()}',
                                      style='red')
                    else:
                        console.print(f'No revenue on [bold]future[/bold]\
                                      date {report_date_from.date()}',
                                      style='red')
                    return

                sales = 0
                with open(os.getcwd()+'\\sold.csv', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        sell_date = dt.strptime(row['sell_date'],
                                                '%Y-%m-%d')
                        if report_date_from <= sell_date <= report_date_until:
                            sales += float(row['sell_price'])

                if args.now:
                    console.print('Today\'s revenue (so far): \u20ac{:0.2f}'
                                  .format(sales), style='green')
                elif args.yesterday:
                    console.print('Yesterday\'s revenue: \u20ac{:0.2f}'
                                  .format(sales), style='green')
                elif not args.month and not args.year:
                    console.print(f'Revenue for {report_date_from.date()}: '
                                  + '\u20ac{:0.2f}'.format(sales),
                                  style='green')
                else:
                    console.print(f'Revenue from {report_date_from.date()} '
                                  + f'until {report_date_until.date()}: '
                                  + '\u20ac{:0.2f}'.format(sales),
                                  style='green')

            except OSError:
                console.print('Not able to report revenue', style='red')
                return

        elif args.type == 'profit':
            report_date_until = dt.strptime(report_date, '%Y-%m-%d')
            if args.month:
                report_date_from = report_date_until.replace(day=1)
            elif args.year:
                report_date_from = report_date_until.replace(month=1, day=1)
            else:
                report_date_from = report_date_until

            try:
                if report_date_from > dt.today():
                    if args.month or args.year:
                        console.print(f'No profit for [bold]future[/bold]\
                                      date-range {report_date_from.date()}\
                                      until {report_date_until.date()}',
                                      style='red')
                    else:
                        console.print(f'No profit on [bold]future[/bold]\
                                      date {report_date_from.date()}',
                                      style='red')
                    return

                profit = 0
                with open(os.getcwd()+'\\sold.csv', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        check_date = dt.strptime(row['sell_date'],
                                                 '%Y-%m-%d')
                        if report_date_from <= check_date <= report_date_until:
                            profit += float(row['sell_price'])

                            with open(os.getcwd()+'\\bought.csv', newline='')\
                                 as csvfile:
                                reader_bought = csv.DictReader(csvfile)
                                for row_bought in reader_bought:
                                    if row_bought['id'] == row['bought_id']:
                                        profit -= float(row_bought
                                                        ['buy_price'])

                if args.now:
                    console.print('Today\'s profit (so far): \u20ac{:0.2f}'
                                  .format(profit), style='green')
                elif args.yesterday:
                    console.print('Yesterday\'s profit: \u20ac{:0.2f}'
                                  .format(profit), style='green')
                elif not args.month and not args.year:
                    console.print(f'Profit for {report_date_from.date()}: '
                                  + '\u20ac{:0.2f}'.format(profit),
                                  style='green')
                else:
                    console.print(f'Profit from {report_date_from.date()} '
                                  + f'until {report_date_until.date()}: '
                                  + '\u20ac{:0.2f}'.format(profit),
                                  style='green')

            except OSError:
                console.print('Not able to report profit', style='red')
                return

    else:
        return


if __name__ == '__main__':
    main()
    pass
