
import subprocess, sys

def find_path():
    client_os = sys.platform
        
    if client_os == "linux":
        result = subprocess.run(["whereis", "buildpan"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode == 0:
            result = result.stdout.decode()
            path = result.strip()
            find_path.file_path = path[10:-9]
    
    # return file_path
            