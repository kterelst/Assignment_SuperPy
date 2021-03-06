# This module will create all permanent files with headers for later use
# in super.py if they don't exist yet. The files are placed in the current
# directory.
#
# - bought.csv
# - sold.csv
# - id.csv
# - reportdate.csv

import os
import csv
from datetime import date
from pathlib import Path
from .date_functions import *
from .id_number import *
from .reporting import *
from .validations import *


def initialize_files():  # for first-time use
    current_dir = Path(os.getcwd())
    # add file bought.csv for goods bought
    if not os.path.isfile(current_dir / 'bought.csv'):
        fieldnames = ['id', 'product_name', 'buy_date', 'buy_price',
                      'expiration_date', 'sold_id']
        with open(current_dir / 'bought.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    # add file sold.csv for goods sold
    if not os.path.isfile(current_dir / 'sold.csv'):
        fieldnames = ['id', 'product_name', 'sell_date', 'sell_price',
                      'bought_id']
        with open(current_dir / 'sold.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    # add file id.csv to increase id-number for every good bought or sold
    if not os.path.isfile(current_dir / 'id.csv'):
        bought_id = 0
        sold_id = 0
        fieldnames = ['bought_id', 'sold_id']
        with open(current_dir / 'id.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'bought_id': bought_id, 'sold_id': sold_id})
    # add file reportdate.csv to keep track of requested report date
    if not os.path.isfile(current_dir / 'reportdate.csv'):
        fieldnames = ['report_date']
        with open(current_dir / 'reportdate.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'report_date': date.today().strftime('%Y-%m-%d')})


initialize_files()
