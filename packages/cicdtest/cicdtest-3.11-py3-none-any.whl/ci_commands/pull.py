"""
    Title: pull.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 11-09-2021
    Description:
        ###############################################################
        ## Check for pull operation on a repository   ## 
         ###############################################################
 """

from buildpan.previous_commit import prev_commit
import requests
from buildpan import setting, workflow, repo_pull, find_path
import click
import os


info = setting.info


# getting env variable
push_commit = info["PUSH_COMMIT_URL"]


@click.command()
def pull():
    '''
    For initiating the pull operation

    \f
    '''
    
    # pull

    all_repo_name = []
    
    try:
        find_path.find_path()
        file_path = find_path.find_path.file_path
        file_path = file_path + "/info.txt"
        print(file_path)
        var = file_path
        # reading data from centralized file
        with open(file_path) as file:
            print("in")
            info = file.readlines()
            print(info)
            for data in info:
                print("data = ", data)
                d = eval(data)
                print(d)
                repo_name = d["repo_name"]
                repo_name_compare = repo_name.lower()
                repo_name = "repo_name="+repo_name.lower()
                all_repo_name.append(repo_name)
                
                # using pooling for pull operation
                response = requests.get(push_commit, repo_name)
                
                res=response.content
                res=str(res)
                index=res.index("'")
                index1=res.index("'",index+1)
                res=res[index+1:index1]
                res = res.lower()
                var = var + res
                
                if repo_name_compare == res:
                    path = d["path"]
                    project_id = d["project_id"]
                    username = d["username"]

                    # doing pull operation
                    repo_pull.repo_pull(path, project_id, repo_name_compare, username)
                    var = var + "called"
                            
                    # if pull success calling deployment        
                    response = workflow.workflows(path)
                    var = var + str(response)
                    
                    # if deployment fails go to previous commit
                    if response == False:
                        prev_commit(path, repo_name)
    
    except Exception as e:
        print("Exception = ", e)
 

    with open("process.txt", "a") as file:
         file.write(var + "\n")



