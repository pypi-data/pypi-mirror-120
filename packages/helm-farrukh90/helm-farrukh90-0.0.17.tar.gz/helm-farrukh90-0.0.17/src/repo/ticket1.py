import os 
import sys

from Classes.shared_scripts.modules import sizechecker
sys.path.append('../')

from shared_scripts.modules import filechecker, folderchecker

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
    folderchecker("~/web")
    folderchecker("~/web/charts")
    folderchecker("~/web/templates")
    filechecker("~/web/Chart.yaml")
    sizechecker("~/web/Chart.yaml")
    filechecker("~/web/values.yaml")
    sizechecker("~/web/values.yaml")