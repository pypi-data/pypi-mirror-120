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
import os
from ci_commands import encrypt

def create_file(project_id, repo_name, path, username):
    try:
        file_path = os.getenv('file_path')
        # enc_key = b'CgOc_6PmZq8fYXriMbXF0Yk27VT2RVyeiiobUd3DzR4='
        # find_path.find_path()
        # file_path = find_path.find_path.file_path

        all_project_id = []

        dict = {
                "project_id": project_id,
                "repo_name": repo_name,
                "path": str(path),
                "username": username
        }


        with open(f"{file_path}/info.txt") as file:
            info = file.readlines()
            data = eval(info)
            all_project_id.append(data['project_id'])
            
        if project_id in all_project_id:
            print("repository already initialized")
        else:
            
            with open(f"{file_path}/info.txt", "a") as file:
                file.write(str(dict) + "\n")
        
        # # encrypting a json file
        # enc = encrypt.Encryptor()
        # enc.encrypt_file(enc_key, f"{file_path}/info.txt")
    
    except Exception as e:
        print(e)
