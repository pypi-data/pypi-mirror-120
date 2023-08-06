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
    client_os = sys.platform
    
    if client_os == "linux":
        var = subprocess.run("whereis buildpan", shell=True, encoding='UTF-8')
        print(var.stdout)
        #cron_job = CronTab(user=True)
        #cron_path = os.environ.get()
    # job = cron_job.new(command=f'{cron_path} pull')
    # job.minute.every(1)
    # cron_job.write()