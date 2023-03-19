import subprocess
import os
from typing import List
import datetime
import math
import sys
import time
from Project import Project
from enums import OS, ErrorType
from Logger import Logger


class SonarScanner:

    def __init__(self, url: str, os: OS, projects: List[Project]):
        self.url = url
        self.os = os
        self.projects = projects

    def prepareScannerCommand(self, project_key, token, location) -> None:
        scan_command = []

        if (self.os == OS.WINDOWS.value):
            scan_command = f'sonar-scanner.bat -D"sonar.projectKey={project_key}" -D"sonar.sources={location}" -D"sonar.host.url={self.url}" -D"sonar.login={token}"'
        elif (self.os == OS.LINUX.value or self.os == OS.MAC.value):
            scan_command = f'sonar-scanner -Dsonar.projectKey={project_key} -Dsonar.sources={location} -Dsonar.host.url={self.url} -Dsonar.login={token}'
        else:
            raise Exception("Error: Unknown OS.")
        return scan_command

    def run(self) -> None:
        for project in self.projects:
            projectPath = project.prepareProject()
            scan_command = self.prepareScannerCommand(
                project_key=project.project_key, token=project.token, location=projectPath)
            try:
                output = subprocess.run(
                    scan_command, stdout=subprocess.PIPE, text=True)
            except subprocess.CalledProcessError:
                return Logger.create(errorType=ErrorType.RUN)

    def multiRun(self) -> None:
        process_limit = 1
        project_index = 0
        resultRaport = {}
        for index in range(0, math.ceil(len(self.projects)/process_limit)):
            process = []
            projectRangeIndex = project_index+process_limit
            if (projectRangeIndex > len(self.projects)):
                projectRangeIndex = len(self.projects)

            for project in self.projects[project_index:projectRangeIndex]:
                project_index += 1
                projectPath = project.prepareProject()
                scan_command = self.prepareScannerCommand(
                    project_key=project.project_key, token=project.token, location=projectPath)
                process.append([project.project_key, subprocess.Popen(
                    scan_command, stdout=subprocess.PIPE, text=True)])
            for p in process:
                try:
                    # clear output
                    os.system('cls' if os.name == 'nt' else 'clear')
                    stout, stderr = p[1].communicate()

                    if ("EXECUTION SUCCESS" in stout):
                        resultRaport[p[0]] = {
                            "status": "success",
                            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        }
                        print(f"[SUCCESS] {p[0]}")
                        sys.stdout.flush()
                        time.sleep(1)
                    else:
                        resultRaport[p[0]] = {
                            "status": "error",
                            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        }
                        Logger.saveErrorLogs(
                            errorLogs=stout, project_key=p[0])
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f"[ERROR] {p[0]}")
                        sys.stdout.flush()
                        time.sleep(1)
                except subprocess.CalledProcessError:
                    return Logger.create(errorType=ErrorType.RUN)
        Logger.saveResultLogs(resultLogs=resultRaport)
        return resultRaport
