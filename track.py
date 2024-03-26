#!/usr/bin/python
# imports
import argparse
import time
import os
import datetime
import os.path as path
import shutil
from rich import print,  pretty
import platform
import psutil
import sys

# Permanent Variables
system = platform.system()
now = datetime.datetime.now()
current_date = datetime.datetime.now().date()
current_date = "{:02d}-{:02d}-{:04d}".format(
        current_date.day,
        current_date.month,
        current_date.year
        )
time_now = datetime.datetime.now().time()
current_time = "{:02d}:{:02d}".format(time_now.hour, time_now.minute)
def_date = str(round(int(datetime.datetime.now().strftime("%Y")),  -1)) + "s/" + datetime.datetime.now().strftime("%Y") + "/" + datetime.datetime.now().strftime("%b") + "/" + datetime.datetime.now().strftime('%d-%m-%Y')

# Changable Variables
if system == "Windows":
    logs_dir = os.getenv('USERPROFILE').replace('\\',  '/')
    +"/Desktop/.dlogs/.Track/"
else:
    logs_dir = os.getenv('HOME')+"/.dlogs/.Track/"

# Initiate ArgumentParser
parser = argparse.ArgumentParser()
parser.add_argument('-n', default="UNTITLED", help="name of the task", type=str)
parser.add_argument('-i', default="No desc", help="Describe the task", type=str)
parser.add_argument('-c', help="Check logs", action='store_true')
parser.add_argument('-r', help="Read logs",action='store_true')
parser.add_argument('-s', help="start stopwatch",action='store_true',default=True)
parser.add_argument('-m', help="Summarise log file",action='store_true')
parser.add_argument('-d', default=current_date, help="date to check for", type=str)
args = parser.parse_args()
start = args.s
name = args.n
info = args.i
check = args.c
date = args.d
summarise = args.m
read_l = args.r

# Check if Directory exists
if not path.exists(logs_dir):
    os.makedirs(logs_dir)

# Functions
# Check if Script is already running


def is_running(script: str):
    for q in psutil.process_iter():
        if q.name().startswith('python'):
            if len(q.cmdline()) > 1 and script in q.cmdline()[1] and q.pid != os.getpid():
                return True
    return False
# Clear Terminal command


def clear():
    if system == "Windows":
        os.system('cls')
    else:
        os.system('clear')
# Print Commands


def print_center_timer(text: str):
    center_line = int(shutil.get_terminal_size().lines/2-text.count('\n')+1)
    s = text.center(shutil.get_terminal_size().columns-text.count(' '))
    print('\n'*center_line, s, '\n'*center_line, end="\r")


def print_center_text(text: str):
    center_line = int(shutil.get_terminal_size().lines/2-text.count('\n')+1)
    print('\n'*center_line)
    ltext = text.splitlines()
    for line in ltext:
        s = line.center(shutil.get_terminal_size().columns)
        print(s)
    print('\n'*center_line)
    if system == "Windows":
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
# Main Functions


def stopwatch():
    if not os.path.exists(f"{logs_dir}/{def_date}"):
        os.makedirs(f"{logs_dir}/{def_date}")
    if not os.path.isfile(f"{logs_dir}/{def_date}/track.md"):
        f = open(f"{logs_dir}/{def_date}/track.md",  "a")
        f.write("| Name | Description | Start | End | Duration |")
        f.write('\n')
        f.write("| :---:" * 5)
        f.write("|")

    running = True
    seconds = 0
    start_time = datetime.datetime.now().time()
    while running:
        try:
            mins, secs = divmod(seconds, 60)
            hours, mins = divmod(mins, 60)
            timer = "{:02d}:{:02d}:{:02d}".format(hours, mins, secs)
            clear()

            print_center_timer(timer)
            time.sleep(1)
            seconds += 1
        except KeyboardInterrupt:
            end_time = datetime.datetime.now().time() 
            end_td = datetime.timedelta(hours=end_time.hour,minutes=end_time.minute,seconds=end_time.second)
            start_td = datetime.timedelta(hours=start_time.hour,minutes=start_time.minute,seconds=start_time.second)
            dur = end_td-start_td
            dur = datetime.datetime.strptime(str(dur), "%H:%M:%S")
            duration = "{:02d}:{:02d}:{:02d}".format(dur.hour, dur.minute, dur.second)
            td = datetime.timedelta(hours=dur.hour, minutes=dur.minute, seconds=dur.second)
            start_time = "{:02d}:{:02d}".format(start_time.hour,  start_time.minute)
            end_time = "{:02d}:{:02d}".format(end_time.hour,  end_time.minute)
            write_data = f"\n| {name.upper()} | {info.upper()} | {start_time} | {end_time} | {duration} |"
            with open(f"{logs_dir}/{def_date}/track.md",  'a') as f:
                f.write(write_data)
            clear()
            print_center_text(
                    f"{name.upper()} | {info.upper()} | {start_time} | {end_time} | {duration}"
                    )
            running = False


def check_log(date):
    month = datetime.datetime.strptime(date,  "%d-%m-%Y").strftime("%b")
    year = datetime.datetime.strptime(date,  "%d-%m-%Y").strftime("%Y")
    decade = str(round(int(year),  -1))
    path = f"{logs_dir}/{decade}s/{year}/{month}/{date}"
    if os.path.exists(path):
        log_read = open(f"{path}/track.md", 'r')
        data = log_read.read()
        log_read.close()
        return data


def read_log(date,   name):
    start_times = []
    end_times = []
    durations = []
    durs = []
    descriptions = []
    tds = datetime.timedelta()
    data = check_log(date)
    data = data.splitlines()
    for line in data:
        line_l = line.split(' | ')
        if line_l[0] == f'| {name.upper()}':
            start_times.append(line_l[-3])
            end_times.append(line_l[-2])
            durations.append(line_l[-1])
            descriptions.append(line_l[1])
    for duration in durations:
        duration = duration.replace(" |",  "")
        dur = datetime.datetime.strptime(duration,  '%H:%M:%S')
        td = datetime.timedelta(
                hours=dur.hour,
                minutes=dur.minute,
                seconds=dur.second
                )
        durs.append(td)
        tds += td
    return start_times, end_times, tds, durs, descriptions


def Summarise(date):
    data = check_log(date)
    names = []
    lines = data.splitlines()
    lines.pop(0)
    lines.pop(0)
    ltds = []
    for line in lines:
        lsp = line.split(' | ')
        nm = lsp[0].replace('| ',  '')
        if nm not in names:
            names.append(nm)
    for name in names:
        tds = read_log(date,  name)[-1]
        ltds.append(tds)
    return ltds, names


# Execute as script
if __name__ == "__main__":
    pretty.install()
    if check:
        data = check_log(date)
        clear()
        print_center_text(data)
    elif read_l:
        start_times, end_times, tds, durs,descs= read_log(date,  name)
        # clear()
        output = f"{name.upper()} | {descs[0]} | {start_times[0]} | {end_times[0]} | {durs[0]} |\n"
        whitespaces = len(name)+1
        for i in range(1,  len(start_times)):
            output += ' '*whitespaces
            output += f"| {descs[i]} | {start_times[i]} | {end_times[i]} | {durs[0]} |\n"

        output += f"TOTAL DURATION  =  {tds}"
        print(output)
        # print_center_text(output)
    elif summarise:
        ltds,  names = Summarise(date)
        lenf = len(ltds)
        month = datetime.datetime.strptime(date,  "%d-%m-%Y").strftime("%b")
        year = datetime.datetime.strptime(date,  "%d-%m-%Y").strftime("%Y")
        decade = str(round(int(year),  -1))
        path = f"{logs_dir}/{decade}s/{year}/{month}/{date}"
        output = ""
        for i in range(0,  lenf):
            output += f"| {names[i]} | {ltds[i]} |\n"
        with open(f"{path}/summary.md",  "w") as f:
            f.write("| Name | Duration |\n| :---: | :---: |\n")
            f.write(output)
        clear()
        output = f"| Name | Duration |\n{output}"
        print_center_text(output)
    elif start and not is_running(sys.argv[0]):
        stopwatch()
    elif start and is_running(sys.argv[0]):
        print_center_text(f"'{sys.argv[0]}' Process is already running")
