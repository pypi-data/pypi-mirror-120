


import datetime
from buildpan import yaml_reader, deployer

def workflows(path):
    print("in")
    workflow = yaml_reader.yaml_reader.workflow
    jobs = yaml_reader.yaml_reader.jobs

    success = False
    print("called")
    start_time = datetime.datetime.now()
    for job in workflow:
        if job == "scripts":
            success = deployer.script_runer(jobs[job], path)
        
        elif job == "deploy":
            if jobs[job]['appName'].lower() == 'Meanstack'.lower():
                success = deployer.mean_stack(path)
            else:
                success = False
                print(f"{jobs[job]['appName']} is not Supported")
                break
        else:
            success = False

    return success