import json
import os
from typing import List
import datetime
from enums import ErrorType


currentPath: str = os.getcwd()
timeStamp: str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


class Logger(Exception):

    logs: dict = {}
    logDirectory: str = "logs"
    logDirectoryPath: str

    def __init__(self) -> None:
        logFolder = os.path.join(currentPath, self.logDirectory)
        # check if folder not exists
        if (os.path.exists(logFolder) == False):
            os.mkdir(self.logDirectory)
        # define file directory
        self.logDirectoryPath = logFolder

    @staticmethod
    def throwError(errorType: ErrorType, message: str = "") -> None:
        raise Logger.create(errorType=errorType, message=message)

    @staticmethod
    def saveResultLogs(resultLogs: dict, fileDirectory: str = "logs") -> None:
        relativePath = os.path.join(fileDirectory, timeStamp)
        if (os.path.exists(relativePath) == False):
            os.mkdir(relativePath)

        with open(f"{relativePath}/result.json", "w", encoding="utf-8") as f:
            json.dump(resultLogs, f)

    @staticmethod
    def saveErrorLogs(errorLogs: any, project_key: str, fileDirectory: str = "logs") -> None:
        # define file name by date
        relativeFolderPath = os.path.join(fileDirectory, timeStamp)
        relativeFilePath = os.path.join(
            relativeFolderPath, project_key+"-error"+".txt")
        # check if folder not exists
        if (os.path.exists(relativeFolderPath) == False):
            os.mkdir(relativeFolderPath)

        with open(relativeFilePath, "w", encoding="utf-8") as f:
            f.write(errorLogs)

    def prepareLogs(self, project_key: str, errorType: ErrorType, message: str) -> None:
        # check if project key not exists
        if (project_key not in self.logs.keys()):
            self.logs[project_key] = []
        # add log
        self.logs[project_key].append({
            "errorType": errorType.value,
            "message": message
        })
        self.saveLog()

    def getPrevProjectLogs(self) -> List[str]:
        # list all files in logs directory
        folders = [f.name for f in os.scandir(os.path.join(
            currentPath, self.logDirectory)) if f.is_dir()]
        if (len(folders) == 0):
            return {}
        # sort folders by date
        folders.sort(reverse=True)
        # get first folder
        firstFolder = folders[0]
        # get first folder path
        firstFolderPath = os.path.join(self.logDirectory, firstFolder)
        with open(os.path.join(firstFolderPath, "result.json"), "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def create(errorType: str, message: str = "") -> str:
        if (errorType == ErrorType.CLONE):
            message = f"{errorType}-Error: while cloning project. {message}"
        elif (errorType == ErrorType.PREPARE):
            message = f"{errorType}-Error: while preparing project. {message}"
        elif (errorType == ErrorType.RUN):
            message = f"{errorType}-Error: while running project. {message}"
        elif (errorType == ErrorType.GITHUB):
            message = f"{errorType}-Error: while getting project from github. {message}"
        elif (errorType == ErrorType.SONARSCANNER):
            message = f"{errorType}-Error: while running sonarscanner. {message}"
        else:
            message = f"{errorType}-Error: Unknown error. {message}"

        return message
