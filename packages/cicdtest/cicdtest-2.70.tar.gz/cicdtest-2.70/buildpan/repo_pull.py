"""
    Title: repo_pull.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 13-09-2021
    Description:
        ###############################################################
        ## Perform a pull operation on a repository   ## 
         ###############################################################
 """

import git
import datetime
import requests
from buildpan import setting


info = setting.info


fetch_log = info["FETCH_LOG_URL"]


def repo_pull(path, project_id, repo_name, username):

    try:
        print(path)
        repo_name = git.Repo(path)
        origin = repo_name.remote(name='origin')
        origin.pull()
        print("success")
        curtime = datetime.datetime.now()          
        requests.post(fetch_log,data={'project_id':project_id,'repo_name':repo_name,'Time ':curtime,'user_name':username,'message':"pull success",'status':'pull operation performed'})
    
    except Exception as e:
        print("e = ",e)
        # curtime = datetime.datetime.now()          
        # requests.post(fetch_log,data={'project_id':project_id,'repo_name':repo_name,'Time ':curtime,'user_name':username,'message':"pull failed",'status':'pull operation performed'})
