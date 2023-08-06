"""
    Title: github_webhook.py
    Author: Akash D.
    Modified By: Kushagra A.
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 21-09-2021
    Description:
        ###############################################################
        ## Create a webhook on a specific repository   ## 
         ###############################################################
 """

from buildpan.installer import installer
from logging import info
import requests, datetime
from github import Github
from buildpan import setting, create_file



ENDPOINT = "webhook"

info = setting.info

fetch_log = info["FETCH_LOG_URL"]
host = info["HOST"]
fetch_log = info["FETCH_LOG_URL"]
         
def github(project_id, path, token, username, repo_name):
    
    try:
        EVENTS = ["*"]      # Events on github
       
        config = {
            "url": f"http://{host}/{ENDPOINT}",
            "content_type": "json"
        }
    
        # login to github account
        
        g = Github(token)
        
        # accessing a particular repository of a account
        repo = g.get_repo(f"{username}/{repo_name}")
        print(repo)

        curtime = datetime.datetime.now()
        # creating a webhook on a particular repository
        try:
            repo.create_hook("web", config, EVENTS, active=True)

            requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=webhook created for repository - '+repo_name+'&status=success&operation=webhook')

            installer()
            # create file
            create_file.create_file(project_id, repo_name, path, username)

          
        except Exception as e:
            print("webhook already exists on this repository ")
            requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Exception: webhook already exists for repository - '+repo_name + '. '+ str(e)+'&status=success&operation=webhook')
            
            installer()

            # create file
            create_file.create_file(project_id, repo_name, path, username)

          
    except Exception as e:
        print("exception occured = ", e)
        requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Exception: webhook creation failed for repository - '+repo_name+ '. '+ str(e)+'&status=failed&operation=webhook')


