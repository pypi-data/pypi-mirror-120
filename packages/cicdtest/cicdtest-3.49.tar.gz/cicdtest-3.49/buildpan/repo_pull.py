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
import subprocess


info = setting.info


fetch_log = info["FETCH_LOG_URL"]


def repo_pull(path, project_id, repo_name, username):

    try:
        subprocess.call(["git", "pull", "origin", "main"], cwd=path)
        # repo = git.Repo(path)
        # origin = repo.remote(name='origin')
        # res=origin.pull()

        curtime = datetime.datetime.now()
        data = {
            'project_id':project_id
        }
        # fetch_log = concat(fetch_log, "?" + 'project_id='+project_id+'&repo_name='+repo_name+'&Time='+curtime+'&user_name='+username+'&message='+"pull success"+'&status='+'pull operation performed')           
        requests.post(fetch_log, data)
    
    except Exception as e:
        print("e = ",e)
        curtime = datetime.datetime.now()          
        requests.post(fetch_log,data={'project_id':project_id,'repo_name':repo_name,'Time ':curtime,'user_name':username,'message':"pull failed",'status':'pull operation failed'})
