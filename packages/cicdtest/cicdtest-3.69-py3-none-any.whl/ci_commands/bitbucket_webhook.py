
"""
    Title: bitbucket_webhook.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 21-09-2021
    Description:
        ###############################################################
        ## Create a webhook on a specific bitbucket repository   ## 
         ###############################################################
 """

import requests
import requests, datetime
from requests.auth import HTTPBasicAuth
from buildpan import create_file, installer
from buildpan import setting

info = setting.info

fetch_log = info["FETCH_LOG_URL"]

         
def bitbucket(project_id, path, refresh_token, key, secret, username, repo_name):
    try:

        access_url = "https://bitbucket.org/site/oauth2/access_token"
        grant_body = {
        "grant_type": 'refresh_token',
        "refresh_token": refresh_token
        }

        # generating access token
        response1 = requests.post(access_url, auth=HTTPBasicAuth(key, secret), data=grant_body)
        token = response1.json()['access_token']

        header = {
            "Authorization": 'Bearer ' + token,
            'Content-Type': 'application/json',

        }
        
        curtime = datetime.datetime.now()
        # creating a webhook on a particular repository
        hook_url = f"https://api.bitbucket.org/2.0/repositories/{username}/{repo_name}/hooks"
        payload_url = "http://35.225.89.124/bit_webhook"

        response3 = requests.get(hook_url, headers=header)
        data = response3.json()['values']
        hook_body = {
            "description": "Webhook Description",
            "url": payload_url,
            "active": True,
            "events": [
                "repo:push",
                "repo:commit_comment_created",
            ]
        }
        uuid = None

        for value in data:
            url = value["url"]

            if payload_url != url or len(data) == 0:
                requests.post(hook_url, headers=header, json=hook_body)

                print("Webhook created")
                requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=webhook created for repository - '+repo_name+'&status=success&operation=webhook')

                installer.installer()

                # create file
                create_file.create_file(project_id, repo_name, path, username)
                break

            else:
                uuid = data[0]["uuid"][1:-1]
                url4 = hook_url + f"/{uuid}"                

                requests.put(url4, headers=header, json=hook_body)
                print("Webhook already exists")

                requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Exception: webhook already exists for repository - '+repo_name +'&status=success&operation=webhook')

                installer.installer()

                # create file
                create_file.create_file(project_id, repo_name, path, username)
                break
          
    except Exception as e:
        print("exception occured ==", e)
        requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Exception: webhook creation failed for repository - '+repo_name+ '. '+ str(e)+'&status=failed&operation=webhook')
