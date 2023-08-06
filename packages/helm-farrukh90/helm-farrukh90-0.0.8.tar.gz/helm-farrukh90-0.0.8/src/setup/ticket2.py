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
        output = subprocess.check_output(["helm", "repo", "list"])
        output = output.decode('utf-8')
        for i in output.splitlines():
            if "stable" in i:
                OUT = i 
        if "stable" in OUT:
            print(bcolors.OKGREEN + "stable repo is added"+ bcolors.ENDC)
            time.sleep(0.5)
        else: 
            print("stable repo is not added")
            sys.exit(1)
            time.sleep(0.5)
    except:
        print(bcolors.FAIL + "stable repo is not added"+ bcolors.ENDC)
        sys.exit(1)
        time.sleep(0.5)
    try:
        output = subprocess.check_output(["helm", "repo", "list"])
        output = output.decode('utf-8')
        for i in output.splitlines():
            if "jenkins" in i:
                OUT = i 
        if "jenkins" in OUT:
            print(bcolors.OKGREEN + "jenkins repo is added"+ bcolors.ENDC)
            time.sleep(0.5)
        else: 
            print(bcolors.FAIL + "jenkins repo is not added"+ bcolors.ENDC)
            sys.exit(1)
            time.sleep(0.5)
    except:
        print(bcolors.FAIL + "jenkins repo is not added"+ bcolors.ENDC)
        sys.exit(1)
        time.sleep(0.5)
    try:
        output = subprocess.check_output(["helm", "repo", "list"])
        output = output.decode('utf-8')
        for i in output.splitlines():
            if "hashicorp" in i:
                OUT = i 
        if "hashicorp" in OUT:
            print(bcolors.OKGREEN + "hashicorp repo is added"+ bcolors.ENDC)
            time.sleep(0.5)
        else: 
            print(bcolors.FAIL + "hashicorp repo is not added"+ bcolors.ENDC)
            sys.exit(1)
            time.sleep(0.5)
    except:
        print(bcolors.FAIL + "hashicorp repo is not added"+ bcolors.ENDC)
        sys.exit(1)
        time.sleep(0.5)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
taskchecker()