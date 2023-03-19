from enum import Enum

class OS(Enum):
    WINDOWS = "win"
    LINUX = "linux"
    MAC = "mac"


class Source(Enum):
    GIT = "git-remote"
    LOCAL = "local"


class ErrorType(Enum):
    CLONE = "clone"
    PULL = "pull"
    PREPARE = "prepare"
    RUN = "run"
    GITHUB = "github"
    CONFIG = "config"
    SONARSCANNER = "sonarscanner"
