SuperPY - ReadMe

In this user guide you can find the following information:
- Intended use
- Technical details
- Requirements
- User interface
- How to use
- Filesystem
- Recommendations
- Contact details


Technical details:
------------------
This program was tested for use on Windows.
It will not work on all Operating Systems.
The use of \ is widely used and i.e. Apple has a different view on that.


Requirements:
-------------
A requirements.txt is included


Intended use:
-------------
A software package for the retail industry.
You will be able to record purcheses and sales.
You will be able to report inventory, revenue and profit.


User interface:
---------------
A choice was made to make this a 'command-line-interface' program.
This means you can run it in from the command line on a computer (i.e. Windows
Powershell or Terminal application).
The commands will be passed to the program with one line, with every argument
seperated bij a space.


How to use:
-----------
Record a purchase:
python super.py buy --product-name orange --price 0.8 --expiration-date 2020-01-01

Record a sale:
python super.py sell --product-name orange --price 2

Change the date-setting for all reports. This only applies when 1 date is used.
For periods (month, year) the argument must be in the specific report command.
python super.py --date 2021-03-16
python super.py report --now
python super.py report inventory --yesterday
python super.py report revenue --month 2021-03
python super.py report profit --year 2021

Change the date by adding or deducting days from set date:
python super.py --advance-time -2
python super.py report inventory --advance-time 1

Report inventory:
When chosen for month or year, the last day of it will be chosen.
python super.py report inventory --today

Report revenue:
When chosen for month or year, the entire period will be chosen.
python super.py report revenue --date 2021-03-14

Report profit:
When chosen for month or year, the entire period will be chosen.
python super.py report profit --month 2021-02

Report all sales recorded:
python super.py report sell
- date arguments are not used

Report all purchases recorded:
python super.py report buy
- date arguments are not used

Exporting a report:
Add --excel(-e) or --csv(-c) after your command
python super.py report inventory --date 2021-03-14 -e -c

In time the files could get big and performance will slow down.
For quitting the current command press CTRL+C.
Know that your function at this time will not be (entirely) performed.


Filesystem:
-----------
In your current directory the next files will be used:
- permanent files (created at first run of the program)
    - bought.csv
    - sold.csv
    - id.csv
    - reportdate.csv
- temporary files (will be deleted after use)
- exported files (timestamped .csv / .xlsx)


Recommendations:
----------------
- Always run commands from the same directory for your shop
- For another shop you can use a different directory
- For full experience of this program, use a multicolor command line interface
- When stuck using commands, use -h to get help
- Do not change the permanent files, this could corrupt the filesystem


Contact details:
----------------
This program was made by Kittie de Jong - ter Elst.
You can reach me by e-mail at kittieterelst@hotmail.com