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

        dict = {
                "project_id": project_id,
                "repo_name": repo_name,
                "path": str(path),
                "username": username
        }
        

        with open(f"{file_path}/info.txt", "a") as file:
            file.write(str(dict) + "\n")
        
        # # encrypting a json file
        # enc = encrypt.Encryptor()
        # enc.encrypt_file(enc_key, f"{file_path}/info.txt")
    
    except Exception as e:
        print(e)
