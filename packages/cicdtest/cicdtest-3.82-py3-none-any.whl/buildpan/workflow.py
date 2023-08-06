"""
    Title: workflow
    Author: Abizer
    Modified By: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 22-09-2021
    Description:
        ###############################################################
        ##      Calls deployer for workflow process                  ## 
        ###############################################################
 """

from buildpan import yaml_reader, deployer

def workflows(path, project_id, repo_name, username):
    
    try:
        yaml_reader.yaml_reader(path)
        workflow = yaml_reader.yaml_reader.workflow
        jobs = yaml_reader.yaml_reader.jobs

        success = False
        
        for job in workflow:
            if job == "scripts":
                success = deployer.script_runer(jobs[job], path)
            
            elif job == "deploy":
                if jobs[job]['appName'].lower() == 'Meanstack'.lower():
                    success = deployer.mean_stack(path, project_id, repo_name, username)
                else:
                    success = False
                    print(f"{jobs[job]['appName']} is not Supported")
                    break
            else:
                success = False
        return success
    
    except Exception as e:
        print(e)