"""
    Title: create_file.py
    Author: Kushagra A.
    Language: Python
    Date Created: 11-09-2021
    Date Modified: 11-09-2021
    Description:
        ###############################################################
        ## Create a file on a specified path   ## 
         ###############################################################
 """

from buildpan import find_path
import json
import os

def create_file(project_id, repo_name, path, username):
    try:
        find_path.find_path()
        file_path = find_path.find_path.file_path
        print(file_path)

        os.environ['central_file_path'] = str(file_path)

        dict = {
                "project_id": project_id,
                "repo_name": repo_name,
                "path": str(path),
                "username": username
        }
        

        with open(f"{file_path}/info.txt", "a") as file:
            file.write(str(dict) + "\n")
    
    except Exception as e:
        print(e)
