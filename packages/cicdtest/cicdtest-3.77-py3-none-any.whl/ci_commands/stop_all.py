"""
    Title: stop_all
    Author: Kushagra A.
    Modified By: Kushagra A.
    Language: Python
    Date Created: 22-09-2021
    Date Modified: 21-09-2021
    Description:
        ###############################################################
        ##      Remove all repo details from centralized file        ## 
        ###############################################################
"""

import click
from click.decorators import command
import os
from buildpan import find_path

@click.command()
def stop_all():
    '''
    For deleting all repository information
    \f
    
   
    '''

    find_path.find_path()
    file_path = find_path.find_path.file_path

    if os.path.exists(file_path + "/info.txt"):
        os.remove(file_path + "/info.txt")
        print("File Deleted!")
    
    else:
        print("File doesn't exists!")