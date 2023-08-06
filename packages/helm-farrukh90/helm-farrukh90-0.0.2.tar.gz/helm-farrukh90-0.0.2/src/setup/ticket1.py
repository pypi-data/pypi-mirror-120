import os 
import subprocess
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
        output = subprocess.check_output(["hsdfelm", "version"])
        if output is not None:
            print(bcolors.OKGREEN +"helm is installed"+ bcolors.ENDC)
        else:
            print(bcolors.FAIL + "did you install helm? "+ bcolors.ENDC)
    except FileNotFoundError:
        print(bcolors.FAIL + "Helm is not installed"+ bcolors.ENDC)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
