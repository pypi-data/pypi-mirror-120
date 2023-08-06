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
import subprocess, sys


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
        result = subprocess.run("whereis buildpan", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = result.stdout.decode()
        file_path = result.strip()
        file_path = file_path[10:-9]
        file_path1 = file_path + "/info. txt"
        # file_path = find_path.find_path()
        print(file_path1)
        var = "path = " + file_path1
        with open(file_path1) as file:
            var = var + "in"
            info = file.readlines()
            var = var + "in2"
        # file_path = find_path.find_path.file_path
        
        # var = var + file_path
        # reading data from centralized file
        # with open(file_path) as file:
        #     info = file.readlines()
        #     for data in info:
        #         d = eval(data)
        #         repo_name = d["repo_name"]
        #         repo_name_compare = repo_name.lower()
        #         repo_name = "repo_name="+repo_name.lower()
        #         all_repo_name.append(repo_name)
                
        #         # using pooling for pull operation
        #         response = requests.get(push_commit, repo_name)
                
        #         res=response.content
        #         res=str(res)
        #         index=res.index("'")
        #         index1=res.index("'",index+1)
        #         res=res[index+1:index1]
        #         res = res.lower()
        #         var = var + res
                
        #         if repo_name_compare == res:
        #             path = d["path"]
        #             project_id = d["project_id"]
        #             username = d["username"]

        #             # doing pull operation
        #             repo_pull.repo_pull(path, project_id, repo_name_compare, username)
        #             var = var + "called"
                            
        #             # if pull success calling deployment        
        #             response = workflow.workflows(path)
        #             var = var + str(response)
                    
        #             # if deployment fails go to previous commit
        #             if response == False:
        #                 prev_commit(path, repo_name)
    
    except Exception as e:
        print("Exception = ", e)
 

    with open("process.txt", "a") as file:
         file.write(var + "\n")



