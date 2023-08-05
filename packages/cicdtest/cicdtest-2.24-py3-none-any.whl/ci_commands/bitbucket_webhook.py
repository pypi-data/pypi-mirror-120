
"""
    Title: bitbucket_webhook.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 13-09-2021
    Description:
        ###############################################################
        ## Create a webhook on a specific bitbucket repository   ## 
         ###############################################################
 """

import requests
import os
from requests.auth import HTTPBasicAuth
from buildpan import create_file, yaml_reader, platform_installer



         
def bitbucket(project_id, path, refresh_token, key, secret, username, repo_name):
    try:
        
        # Before creating
        dir_list = os.listdir(path) 
        print("List of directories and files before creation:")
        print(dir_list)
        print()

        platform_name = yaml_reader.yaml_reader.platform_name
        node_ver = yaml_reader.yaml_reader.platform_ver

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

        if len(data) == 0:
            requests.post(hook_url, headers=header, json=hook_body)

            requests.post("http://35.225.89.124/get_token",
                                    data={"token": token, "name": username, "repo_name": repo_name})
            print("Webhook created")

            if platform_name == "node":
                platform_installer.node_installer(node_ver)
            elif platform_name == "":
                print("Please provide platform name")
            else:
                print("This name is not supported")

           # create file
            create_file.create_file(project_id, repo_name, path, username)

            
        else:
            uuid = data[0]["uuid"][1:-1]
            # print(uuid)

            url4 = hook_url + f"/{uuid}"
            # print(url4)

            requests.put(url4, headers=header, json=hook_body)
            requests.post("http://35.225.89.124/get_token", data={"token": token, "name":username, "repo_name":repo_name})
            print("Webhook already exists")

            if platform_name == "node":
                platform_installer.node_installer(node_ver)
            elif platform_name == "":
                print("Please provide platform name")
            else:
                print("This name is not supported")

            # create file
            create_file.create_file(project_id, repo_name, path, username)

            

          
    except:
        print("exception occured")
