# This module will be able to convert a csv-file into either:
# - A csv-file with name <title>_yyyymmddhhmmss.csv
# - An Excel-file with name <title>_yyyymmddhhmmss.xlsx
# - A table on the console in Rich

import csv
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from openpyxl import Workbook


def print_report(filename, title, args):
    with open(os.getcwd()+f'\\{filename}', newline='') as csvfile:

        console = Console()
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        output_date = datetime.now().strftime('%Y%m%d%H%M%S')

        # export to title_datetime.xlsx
        if args.excel:
            wb = Workbook()
            ws = wb.active
            ws.append(headers)
            for row in reader:
                row_list = []
                row_list.extend(row.values())
                ws.append(row_list)
            output_name = title + '_' + output_date + '.xlsx'
            wb.save(os.getcwd() + '\\' + output_name)
            console.print(f'Output to "[green]{output_name}[/green]"')

        # export to title_datetime.csv
        if args.csv:
            with open(os.getcwd() + f'\\{filename}', newline='') as csvfile:
                console = Console()
                reader = csv.DictReader(csvfile)
                headers = reader.fieldnames
                output_name = title + '_' + output_date + '.csv'
                with open(os.getcwd() + '\\' + output_name, 'w', newline='')\
                        as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(reader)
                    console.print(f'Output to "[green]{output_name}[/green]"')

        # print csv-file in Rich text table
        if not args.excel and not args.csv:
            table = Table(title=title, title_style='bold cyan')
            for header in headers:
                table.add_column(header, justify="right", style="cyan",
                                 no_wrap=True)
            for row in reader:
                row_string = list(row.values())
                table.add_row(*row_string)
            console.print(table)
