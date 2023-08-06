import os 
import subprocess
import sys 
import time
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def taskchecker():
    try:
        output = subprocess.check_output(["helm", "version"])
        if output is not None:
            print(bcolors.OKGREEN +"helm is installed"+ bcolors.ENDC)
            time.sleep(0.5)
        else:
            print(bcolors.FAIL + "did you install helm? "+ bcolors.ENDC)
            sys.exit(1)
            time.sleep(0.5)
    except FileNotFoundError:
        print(bcolors.FAIL + "Helm is not installed"+ bcolors.ENDC)
        sys.exit(1)
        time.sleep(0.5)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
