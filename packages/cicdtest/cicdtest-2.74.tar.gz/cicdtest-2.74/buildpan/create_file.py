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

import os

def create_file(project_id, repo_name, path, username):
    file_path = os.environ.get("file_path")

    dict = {
            "project_id": project_id,
            "repo_name": repo_name,
            "path": str(path),
            "username": username
        }

    with open(f"{file_path}/info.txt", "a") as file:
        file.write(str(dict) + "\n")
