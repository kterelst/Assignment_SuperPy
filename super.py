# Program for recording buy and sale and reporting them

import argparse
import csv
import os
import super_package
from pathlib import Path
from datetime import date
from datetime import datetime as dt
from rich.console import Console

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'


# Your code below this line.
def main():
    args = arguments()
    # print(args)
    commands(args)


def arguments():
    # general
    parser = argparse.ArgumentParser(
             description='supermarket inventory: current, IN and out')
    subparsers = parser.add_subparsers(title='commands', dest='command',
                                       help='sub-command help')

    date_group = parser.add_argument_group()
    date_input_group = date_group.add_mutually_exclusive_group()
    date_input_group.add_argument('--now', '--today', action='store_true',
                                  help='Set date to today for reports')
    date_input_group.add_argument('--yesterday', action='store_true',
                                  help='Set date to yesterday for reports')
    date_input_group.add_argument('--date', type=super_package.valid_date,
                                  help='Set specific date for reports',
                                  metavar='yyyy-mm-dd')
    date_input_group.add_argument('--advance-time', type=int, nargs=1,
                                  help='Number of days forward or backwards\
                                  from last command',
                                  metavar='N')

    # buy and sell commands
    buy_sell = argparse.ArgumentParser(add_help=False)
    buy_sell.add_argument('--product-name', required=True,
                          help='The product name')
    buy_sell.add_argument('--price', type=super_package.valid_float,
                          required=True,
                          help='The price rounded to 2 decimals',
                          metavar='9.99')

    buy_group = subparsers.add_parser('buy', parents=[buy_sell],
                                      help='Put product in inventory\
                                           (You\'ve bought it)')
    buy_group.add_argument('--expiration-date', type=super_package.valid_date,
                           default=9999-12-31, help='The expiration date',
                           metavar='yyyy-mm-dd')

    sell_group = subparsers.add_parser('sell', parents=[buy_sell],
                                       help='Remove product from inventory\
                                            (You\'ve sold it)')

    # reports commands
    reports = ['inventory', 'revenue', 'profit', 'buy', 'sell']
    report_group = subparsers.add_parser('report', help='Display report')
    report_group.add_argument('type', nargs='?', choices=reports,
                              help='Available reports are: '+', '
                              .join(reports), metavar=''+', '.join(reports))
    report_group.add_argument('-e', '--excel', action='store_true',
                              help='Export to Excel')
    report_group.add_argument('-c', '--csv', action='store_true',
                              help='Export to CSV')

    # howto impove? repeating! add parent not possible because -h conflict
    report_date_group = report_group.add_mutually_exclusive_group()
    report_date_group.add_argument('--now', '--today', action='store_true',
                                   help='Set date to today for reports')
    report_date_group.add_argument('--yesterday', action='store_true',
                                   help='Set date to yesterday for reports')
    report_date_group.add_argument('--date', type=super_package.valid_date,
                                   help='Set specific date for reports',
                                   metavar='yyyy-mm-dd')
    report_date_group.add_argument('--month', type=super_package.valid_month,
                                   help='Use specific month for report',
                                   metavar='yyyy-mm')
    report_date_group.add_argument('--year', type=super_package.valid_year,
                                   help='Use specific year for report',
                                   metavar='yyyy')
    report_date_group.add_argument('--advance-time', type=int, nargs=1,
                                   help='Number of days forward or backwards\
                                        from last setting', metavar='N')

    return parser.parse_args()


def commands(args):
    if args.now or args.yesterday or args.date or args.advance_time:
        super_package.change_date(args)

    if args.command == 'buy':
        buy(args)
    elif args.command == 'sell':
        sell(args)
    elif args.command == 'report':
        reports(args)


def buy(args):
    bought_id = super_package.increase_id(args)
    try:
        fieldnames = ['id', 'product_name', 'buy_date', 'buy_price',
                      'expiration_date', 'sold_id']
        line = {'id': bought_id, 'product_name': args.product_name.lower(),
                'buy_date': date.today(), 'buy_price': args.price,
                'expiration_date': args.expiration_date, 'sold_id': None}
        current_dir = Path(os.getcwd())
        with open(current_dir / 'bought.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(line)
        console = Console()
        console.print('Recorded', style='green')
    except OSError:
        console = Console()
        console.print('NOT recorded in bought.csv', style="red")


def sell(args):
    sold_id = super_package.increase_id(args)
    try:
        bought_id_corresponding = super_package.find_bought_id(args, sold_id)
        if bought_id_corresponding:
            fieldnames = ['id', 'product_name', 'sell_date', 'sell_price',
                          'bought_id']
            line = {'id': sold_id, 'product_name': args.product_name.lower(),
                    'sell_date': date.today(), 'sell_price': args.price,
                    'bought_id': bought_id_corresponding}
            current_dir = Path(os.getcwd())
            with open(current_dir / 'sold.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(line)

            console = Console()
            console.print('Recorded', style='green')
        else:
            console = Console()
            console.print('Product not in stock', style='red')
    except OSError:
        console = Console()
        console.print('NOT recorded in sold.csv', style='red')


def reports(args):
    report_date_from, report_date_until = super_package.set_date_range(args)
    if args.type == 'sell':  # not implemented (yet): date-specific
        super_package.print_report('sold.csv', 'Sold', args)
    elif args.type == 'buy':  # not implemented (yet): date-specific
        super_package.print_report('bought.csv', 'Bought', args)
    elif args.type == 'inventory':
        report_inventory(args, report_date_until)
    elif args.type == 'revenue':
        report_revenue(args, report_date_from, report_date_until)
    elif args.type == 'profit':
        report_profit(args, report_date_from, report_date_until)


def report_inventory(args, report_date):
    current_dir = Path(os.getcwd())
    try:
        # check for same prod; write count in tmpinventory.csv
        current_dir = Path(os.getcwd())
        with open(current_dir / 'bought.csv', newline='') as csvfile:
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
                            check_date = report_date

                            # if bought after report_date: skip
                            if dt.strptime(row['buy_date'], '%Y-%m-%d')\
                               > check_date:
                                done_list.append(row['id'])
                            # if expired: skip
                            elif dt.strptime(row['expiration_date'], '%Y-%m-%d'
                                             ) < check_date:
                                done_list.append(row['id'])
                            else:
                                # if sold before report_date: skip
                                if row['sold_id']:
                                    with open(current_dir / 'sold.csv',
                                         newline='') as csvfile:
                                        reader_sold = csv.DictReader(csvfile)
                                        for row_sold in reader_sold:
                                            if (row_sold['id']
                                               == row['sold_id']):
                                                if (dt.strptime(row_sold
                                                    ['sell_date'], '%Y-%m-%d'
                                                     ) <= check_date):
                                                    done_list.append(row['id'])

                        if row['id'] not in done_list:
                            # if same product, price and exp.date: add
                            if (row['product_name'] == new_row['product_name']
                               and row['buy_price'] == new_row['buy_price'] and
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
            fieldnames = ['product_name', 'count', 'buy_price',
                          'expiration_date']
            with open(current_dir / 'tmpinventory.csv', 'w', newline='') \
                 as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(reader_list_new)

        title = 'Inventory' + '_' + str(report_date.date())
        super_package.print_report('tmpinventory.csv', title, args)

    except OSError:
        console = Console()
        console.print('Not able to report inventory', style='red')
        return

    # remove tmpinventory.csv after use
    try:
        os.remove(current_dir / 'tmpinventory.csv')
    except OSError:
        pass  # not a problem if file keeps existing


def report_revenue(args, report_date_from, report_date_until):
    try:
        if report_date_from > dt.today():
            console = Console()
            if args.month or args.year:
                console.print('No revenue for [bold]future[/bold] date-range '
                              + f'{report_date_from.date()} until '
                              + f'{report_date_until.date()}', style='red')
            else:
                console.print('No revenue on [bold]future[/bold] date '
                              + f'{report_date_from.date()}', style='red')
            return

        sales = 0
        current_dir = Path(os.getcwd())
        with open(current_dir / 'sold.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sell_date = dt.strptime(row['sell_date'], '%Y-%m-%d')
                if report_date_from <= sell_date <= report_date_until:
                    sales += float(row['sell_price'])

        console = Console()
        if args.now:
            console.print('Today\'s revenue (so far): \u20ac{:0.2f}'
                          .format(sales), style='green')
        elif args.yesterday:
            console.print('Yesterday\'s revenue: \u20ac{:0.2f}'
                          .format(sales), style='green')
        elif not args.month and not args.year:
            console.print(f'Revenue for {report_date_from.date()}: '
                          + '\u20ac{:0.2f}'.format(sales), style='green')
        else:
            console.print(f'Revenue from {report_date_from.date()} '
                          + f'until {report_date_until.date()}: '
                          + '\u20ac{:0.2f}'.format(sales), style='green')

    except OSError:
        console = Console()
        console.print('Not able to report revenue', style='red')
        return


def report_profit(args, report_date_from, report_date_until):
    try:
        if report_date_from > dt.today():
            console = Console()
            if args.month or args.year:
                console.print('No profit for [bold]future[/bold] date-range '
                              + f'{report_date_from.date()} until '
                              + f'{report_date_until.date()}', style='red')
            else:
                console.print('No profit on [bold]future[/bold] date '
                              + f'{report_date_from.date()}', style='red')
            return

        profit = 0
        current_dir = Path(os.getcwd())
        with open(current_dir / 'sold.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                check_date = dt.strptime(row['sell_date'], '%Y-%m-%d')
                if report_date_from <= check_date <= report_date_until:
                    profit += float(row['sell_price'])

                    with open(current_dir / 'bought.csv', newline='') \
                         as csvfile:
                        reader_bought = csv.DictReader(csvfile)
                        for row_bought in reader_bought:
                            if row_bought['id'] == row['bought_id']:
                                profit -= float(row_bought['buy_price'])

        console = Console()
        if args.now:
            console.print('Today\'s profit (so far): \u20ac{:0.2f}'
                          .format(profit), style='green')
        elif args.yesterday:
            console.print('Yesterday\'s profit: \u20ac{:0.2f}'
                          .format(profit), style='green')
        elif not args.month and not args.year:
            console.print(f'Profit for {report_date_from.date()}: '
                          + '\u20ac{:0.2f}'.format(profit), style='green')
        else:
            console.print(f'Profit from {report_date_from.date()} '
                          + f'until {report_date_until.date()}: '
                          + '\u20ac{:0.2f}'.format(profit), style='green')

    except OSError:
        console = Console()
        console.print('Not able to report profit', style='red')
        return


if __name__ == '__main__':
    main()
