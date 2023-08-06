"""
    Title: start.py
    Author: Kushagra A.
    Language: Python
    Date Created: 10-09-2021
    Date Modified: 21-09-2021
    Description:
        ###############################################################
        ## Create a cron process   ## 
         ###############################################################
 """


import click
from click.decorators import command
from crontab import CronTab
import os


@click.command()
def start():
    '''
    For initiating the cron process 

    \f
    '''
    try:
        PATH = os.getenv("PATH")
        cron_job = CronTab(user=True)
        job = cron_job.new(command=f'export PATH=$PATH:{PATH} && buildpan pull')
        job.minute.every(1)
        cron_job.write()
    except Exception as e:
        print(e)