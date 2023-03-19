import subprocess
import os
import sys
import shutil
from enums import Source, ErrorType
from Logger import Logger
currentPath: str = os.getcwd()


class Project:
    full_path: str = None

    def __init__(self, project_key, token, location, source: Source, branch, git_url=None):
        self.project_key = project_key
        self.token = token
        self.location = location
        self.source = source
        self.git_url = git_url
        self.branch = branch

    def defineFolder(self) -> None:
        # find slash type
        if (self.location.find("/") != -1):
            slash = "/"
        else:
            slash = "\\"
        # find first letter of location
        if (self.location.find(f".{slash}") != -1):
            self.location = self.location.replace(f".{slash}", "")
        elif (self.location[0] == slash):
            self.location = self.location[1:]

        # define full path
        self.full_path = os.path.join(currentPath, "projects", self.location)

    def cloneProject(self) -> str:
        # clone project
        if(os.path.exists(self.full_path)):
            try:
                print("Pulling project")
                sys.stdout.flush()
                subprocess.run(f"git checkout {self.branch}", cwd=self.full_path, capture_output=True, text=True, check=True)
                result = subprocess.run(f"git pull {self.git_url} {self.full_path}",
                                        capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except subprocess.CalledProcessError:
                return Logger.create(errorType=ErrorType.PULL)
        else:   
            try:
                print("Cloning project")
                sys.stdout.flush()
                result = subprocess.run(f"git clone -b {self.branch} {self.git_url} {self.full_path}",
                                        capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except subprocess.CalledProcessError:
                return Logger.create(errorType=ErrorType.CLONE)

    def prepareProject(self) -> None:
        self.defineFolder()
        if (self.source == Source.GIT.value):
            output = self.cloneProject()
            if (output == "Error"):
                return
        elif (self.source == Source.LOCAL.value):
            pass
        else:
            raise Logger.create(errorType=ErrorType.PREPARE)

        return self.full_path

    def getFullProjectPath(self) -> str:
        return self.full_path
