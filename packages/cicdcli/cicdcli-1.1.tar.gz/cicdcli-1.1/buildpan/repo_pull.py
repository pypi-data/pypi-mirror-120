"""
    Title: repo_pull.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 22-09-2021
    Description:
        ###############################################################
        ## Perform a pull operation on a repository   ## 
         ###############################################################
 """

import datetime
import requests
from buildpan import setting
import subprocess


info = setting.info


fetch_log = info["FETCH_LOG_URL"]


def repo_pull(path, project_id, repo_name, username):

    try:
        subprocess.call(["git", "pull", "origin", "main"], cwd=path)

        curtime = datetime.datetime.now()
        requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=pull operation performed'+'&status=success&operation=pull')
    
    except Exception as e:
        print("e = ",e)
        curtime = datetime.datetime.now()          
        requests.post(fetch_log+ "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Exception: pull operation performed. '+str(e)+'&status=failed&operation=pull')
