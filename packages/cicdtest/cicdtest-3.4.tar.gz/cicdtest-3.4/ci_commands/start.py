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
from buildpan import path


@click.command()
def start():
    '''
    For initiating the cron process 

    \f
    '''
    try:
        path.find_path()
        current_path = path.find_path.path
        print(current_path)
        cron_job = CronTab(user=True)
        job = cron_job.new(command=f'{current_path} pull')
        job.minute.every(1)
        cron_job.write()
    except Exception as e:
        print(e)