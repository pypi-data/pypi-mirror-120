"""
    Title: start.py
    Author: Kushagra A.
    Language: Python
    Date Created: 10-09-2021
    Date Modified: 11-09-2021
    Description:
        ###############################################################
        ## Create a cron process   ## 
         ###############################################################
 """


import click
from click.decorators import command
from crontab import CronTab
import os
import sys, subprocess

@click.command()
def start():
    '''
    For initiating the cron process 

    \f
    '''
    try:
        client_os = sys.platform
        
        if client_os == "linux":
            path = subprocess.run("whereis buildpan", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if path.returncode == 0:
                path = path.stdout.decode()
                path = path[10:]
                print(path)
                cron_job = CronTab(user=True)
                job = cron_job.new(command=f'{path} pull')
                print("hi")
                job.minute.every(1)
                print("1")
                cron_job.write()
    except Exception as e:
        print(e)