import os
import csv
from pathlib import Path
from rich.console import Console


def find_bought_id(args, sold_id):  # find same product not sold
    current_dir = Path(os.getcwd())
    try:
        bought_id = None
        with open(current_dir / 'bought.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            reader_list = []
            reader_list.extend(reader)
            for row in reader_list:  # FIFO, if LIFO: reversed(reader_list)
                # find line: not sold, same product
                if not row['sold_id'] and (row['product_name'] ==
                                           args.product_name.lower()):
                    bought_id = int(row['id'])
                    row['sold_id'] = sold_id
                    break
                else:
                    continue
            # rewrite bought.csv with updated sold-field
            fieldnames = ['id', 'product_name', 'buy_date', 'buy_price',
                          'expiration_date', 'sold_id']
            with open(current_dir / 'bought.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(reader_list)
        return bought_id
    except OSError:
        return None


def increase_id(args):
    # increase id-number for buy/sell
    try:
        fieldnames = ['bought_id', 'sold_id']
        current_dir = Path(os.getcwd())
        with open(current_dir / 'id.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # increase current id-number by 1
                if args.command == 'buy':
                    bought_id = int(row['bought_id'])
                    bought_id += 1
                    row['bought_id'] = bought_id
                    id_number = bought_id
                elif args.command == 'sell':
                    sold_id = int(row['sold_id'])
                    sold_id += 1
                    row['sold_id'] = sold_id
                    id_number = sold_id
                else:
                    continue
                # rewrite id.csv with updated id-number for every buy/sell
                with open(current_dir / 'id.csv', 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow(row)
                return id_number
    except OSError:
        console = Console()
        console.print('Failed updating id.csv', style='red')
        return
