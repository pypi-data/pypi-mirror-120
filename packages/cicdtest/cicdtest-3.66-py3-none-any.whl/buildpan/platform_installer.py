"""
    Title: platforminstaller
    Module Name: platforminstaller
    Author: Abizer
    Modified By: Abizer
    Language: Python
    Date Created: 4-09-2021
    Date Modified: 07-09-2021
    Description: diffrent platform installer to be called at init process  
        ###############################################################
        ##                 platform installer                        ## 
        ###############################################################
 """
import subprocess
import sys

def node_installer(node_ver):
    '''
    node installer this function to be called for Linux machine 

    '''
    client_os=sys.platform
    if client_os == "linux":
        subprocess.run("curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash", shell= True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        subprocess.run("source ~/.nvm/nvm.sh", shell= True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,executable='/bin/bash')

        popen_arg = "nvm install "+ node_ver 
        subprocess.call(['/bin/bash', '-i', '-c', popen_arg],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if node_ver != "latest":
            popen_arg = "nvm use "+ node_ver
            subprocess.call(['/bin/bash', '-i', '-c', popen_arg],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    elif client_os == "win32" or client_os == "cygwin":
        popen_arg = "nvm install "+ node_ver 
        subprocess.run(popen_arg ,shell= True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        

        if node_ver != "latest":
            popen_arg = "nvm use "+ node_ver
            subprocess.run(popen_arg ,shell= True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
