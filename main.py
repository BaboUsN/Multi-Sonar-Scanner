import json
import subprocess
from typing import List
import argparse
from Logger import Logger
from enums import ErrorType, Source 
from Project import Project
from Scanner import SonarScanner
import os
import sys
import time
def installationChecker():
    #  check is git installed or not
    try:
        result = subprocess.run(['git', '--version'],
                                capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        Logger.throwError(errorType=ErrorType.GIT,
                          message="Git is not installed.")

    # check is sonar scanner installed or not
    try:
        result = subprocess.run(['sonar-scanner.bat', '--version'],
                                capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        Logger.throwError(errorType=ErrorType.SONARSCANNER,
                          message="Sonnar scanner is not installed.")


def checkPrevProjectLogs(prevProjectLogs, config):
    erroredProjects = []
    for project_key in prevProjectLogs.keys():
        if (prevProjectLogs[project_key]["status"] == "error"):
            erroredProjects.append(project_key)

    willScanProjects = []
    for project in config["projects"]:
        if (project["project_key"] in erroredProjects):
            willScanProjects.append(project)
    return {"erroredProjects": erroredProjects, "willScanProjects": willScanProjects}


def paramProcesser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prev-errored', type=bool, default=False,
                        help='If you want to scan only prev errored projects')
    args = parser.parse_args()
    return args

def checkConfigFile(config):
    configKeys = config.keys()
    if("url" not in configKeys):
        Logger.throwError(errorType=ErrorType.CONFIG, message="url is not defined in config.json")
    if("os" not in configKeys):
        Logger.throwError(errorType=ErrorType.CONFIG, message="os is not defined in config.json")
    if("projects" not in configKeys):
        Logger.throwError(errorType=ErrorType.CONFIG, message="projects is not defined in config.json")
    
    for project in config["projects"]:
        projectKeys = project.keys()
        if("project_key" not in projectKeys):
            Logger.throwError(errorType=ErrorType.CONFIG, message="project_key is not defined in config.json")
        if("token" not in projectKeys):
            Logger.throwError(errorType=ErrorType.CONFIG, message="token is not defined in config.json")
        if("location" not in projectKeys):
            Logger.throwError(errorType=ErrorType.CONFIG, message="location is not defined in config.json")
        if("source" not in projectKeys):
            Logger.throwError(errorType=ErrorType.CONFIG, message="source is not defined in config.json")
        if(project["source"] == Source.GIT.value):
            if("git_url" not in projectKeys):
                Logger.throwError(errorType=ErrorType.CONFIG, message="git_url is not defined in config.json")
            if("branch" not in projectKeys):
                Logger.throwError(errorType=ErrorType.CONFIG, message="branch is not defined in config.json")

def checkAndGetConfig():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except:
        template = {
            "url": "http://localhost:9000",
            "os": "win",
            "projects": [
               {
                    "project_key": "project_key",
                    "token" : "token",
                    "location": "location",
                    "source": "git-remote",
                    "git_url": "git_url",
                    "branch": "branch"
               }   
            ]
        }
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(template, f, indent=4)
        print("config.json file is created. Please fill it.")
        sys.stdout.flush()
        os._exit(0)




if ("__main__" == __name__):
    installationChecker()
    config = checkAndGetConfig()
    checkConfigFile(config)
    logger = Logger()
    args = paramProcesser()
    prevProjectLogs = logger.getPrevProjectLogs()
    if (len(prevProjectLogs.keys()) != 0):
        checkedLogs = checkPrevProjectLogs(prevProjectLogs, config)
        if (len(checkedLogs["erroredProjects"]) != 0 and args.prev_errored == False):
            print(
                "There are some prev errored projects. Do you want to scan them again? (y/n)")
            answer = input()
            if (answer == "y"):
                print("Ok. I will scan only prev errored projects.")
                sys.stdout.flush()
                args.prev_errored = True
            else:
                print("Ok. I will scan all projects.")
                sys.stdout.flush()

        if (args.prev_errored):
            config["projects"] = checkedLogs["willScanProjects"]
        else:
            config["projects"] = config["projects"]
    else:
        print("There is no prev project logs. I will scan all projects.")
        sys.stdout.flush()
    os.system("cls" if os.name == "nt" else "clear")
    print("Do not worry. I will scan all projects.")
    print("Take a moment to savor a delicious cup of coffee and feel the happiness it brings :)")
    print("Scanning projects...")
    time.sleep(2)
    sys.stdout.flush()

    projects: List[Project] = []
    for project in config["projects"]:
        projects.append(Project(project_key=project["project_key"], token=project["token"], location=project["location"],
                        source=project["source"], branch=project["branch"], git_url=project["git_url"]))
    sonarScanner = SonarScanner(
        url=config["url"], os=config["os"], projects=projects)
    resultReport = sonarScanner.multiRun()
    os.system("cls" if os.name == "nt" else "clear")
    print("Results:")
    for result in resultReport.keys():
        if(resultReport[result]["status"] == "success"):
            print(f"[SUCCESS] {result}")
        else:
            print(f"[ERROR] {result}")



