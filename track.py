#!/usr/bin/python
# imports
import argparse
import time
import os
import datetime
import os.path as path
import shutil
from os import system
from rich import print,pretty
# change these variables
logs_dir=os.environ['HOME']+"/.dlogs/.Track/"
def_date=str(round(int(datetime.datetime.now().strftime("%Y")),-1)) + "s/" + datetime.datetime.now().strftime("%Y") + "/" + datetime.datetime.now().strftime("%b") + "/" + datetime.datetime.now().strftime('%d-%m-%Y')
# Fixed variables
now=datetime.datetime.now()
current_date=datetime.datetime.now().date()
current_date="{:02d}-{:02d}-{:04d}".format(current_date.day,current_date.month,current_date.year)
time_now=datetime.datetime.now().time()
current_time= "{:02d}:{:02d}".format(time_now.hour,time_now.minute)
# initiate argeparse
parser=argparse.ArgumentParser()
parser.add_argument('-n', default="unnamed", help="name of the task", type=str)
parser.add_argument('-c',default=False,help="Check logs",type=bool)
parser.add_argument('-r',default=False,help="Read logs",type=bool)
parser.add_argument('-s',default=False,help="start stopwatch",type=bool)
parser.add_argument('-d',default=current_date,help="date to check for",type=str)
args=parser.parse_args()
start=args.s
name=args.n
check=args.c
date=args.d
read_l=args.r
# initiate file
if path.exists(logs_dir)==False:
    os.makedirs(logs_dir)
# functions
clear=lambda: system('clear')
def print_center(text:str):
	center_line=int(shutil.get_terminal_size().lines/2)
	s=text.center(shutil.get_terminal_size().columns) 
	print('\n'*center_line,s,'\n'*center_line,end="\r")
def stopwatch():
	if path.exists(f"{logs_dir}/{def_date}")==False:
		os.makedirs(f"{logs_dir}/{def_date}")
	if path.isfile(f"{logs_dir}/{def_date}/track.md")==False:
		f=open(f"{logs_dir}/{def_date}/track.md","a")
		f.write("| Name | Start | End | Duration |")
		f.write('\n')
		f.write("| :---: | :---: | :---: |")
		f.write('\n')
	else:
		f=open(f"{logs_dir}/{def_date}/track.md","a")
		f.write('\n')

	running=True
	seconds=0
	while running:
		try:
			mins,secs=divmod(seconds,60)
			hours,mins=divmod(mins,60)
			timer="{:02d}:{:02d}:{:02d}".format(hours,mins,secs)
			clear()
			
			print_center(timer)
			time.sleep(1)
			seconds+=1
		except KeyboardInterrupt:
			dur=datetime.datetime.strptime(timer,"%H:%M:%S")
			duration="{:02d}:{:02d}:{:02d}".format(dur.hour,dur.minute,dur.second)
			td=datetime.timedelta(hours=dur.hour,minutes=dur.minute,seconds=dur.second)
			end_time=now+td
			start_time=end_time-td
			start_time="{:02d}:{:02d}".format(start_time.hour,start_time.minute)
			end_time="{:02d}:{:02d}".format(end_time.hour,end_time.minute)
			write_data=f"| {name.upper()} | {start_time} | {end_time} | {duration} |"
			f.write(write_data)
			clear()
			print_center(f"{name.upper()} | {start_time} | {end_time} | {duration}")
			f.close()
			running=False
def check_log(date):
	month=datetime.datetime.strptime(date,"%d-%m-%Y").strftime("%b")
	year=datetime.datetime.strptime(date,"%d-%m-%Y").strftime("%Y")
	decade=str(round(int(year),-1))
	if os.path.exists(f"{logs_dir}/{decade}s/{year}/{month}/{date}"):
		log_read= open(f"{logs_dir}/{decade}s/{year}/{month}/{date}/track.md",'r')
		data=log_read.read()
		log_read.close()
	path=f"{logs_dir}/{decade}s/{year}/{month}/{date}"
	return data
def read_log(date,name):
    start_times=[]
    end_times=[]
    durations=[]
    tds=datetime.timedelta()
    data=check_log(date)
    data=data.splitlines()
    for line in data:
        line_l=line.split(' | ')
        if line_l[0]==f'| {name.upper()}':
            start_times.append(line_l[1])
            end_times.append(line_l[2])
            durations.append(line_l[3])
        for duration in durations:
            dur=datetime.datetime.strptime(duration,'%H:%M:%S |')
            td=datetime.timedelta(hours=dur.hour,minutes=dur.minute,seconds=dur.second)
            tds+=td
    return start_times,end_times,tds

# execute
if __name__=="__main__":
	pretty.install()
	if check:
		data=check_log(date)
		print(data) 
	if start:
		stopwatch()
	if read_l:
		start_times,end_times,tds=read_log(date,name)
		print(f"{name.upper()} | ",end="")
		print(f"{start_times[0]} | {end_times[0]} |")
		whitespaces=len(name)+1
		for i in range(1,len(start_times)):
			print(' '*whitespaces,end="")
			print(f"| {start_times[i]} | {end_times[i]} |")
			print(f"TOTAL DURATION = {tds}")

