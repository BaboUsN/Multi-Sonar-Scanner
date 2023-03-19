

![multiscanner](https://user-images.githubusercontent.com/72748666/226208076-fd23b92c-27ff-4c05-9e82-8c25430bf8db.png)



## What is Multi Sonar Scanner?

Multi Sonar Scanner is a simple tool that allows you to scan multiple SonarQube projects simultaneously. It supports various programming languages such as JS, TS, Go, Python, PHP, and more. This tool helps save time by scanning multiple projects with just one scan.

## How to Use Multi Sonar Scanner?

Using Multi Sonar Scanner is quite easy. You can specify the projects to be scanned by using the command `python main.py --some-option`. There are several useful options available:

-   `--prev-errored`: Scans only previously errored projects.
-   `--multi`: Enables scanning projects as multiple processes.
-   `--process-limit`: Limits the scanning of projects with the desired process limit.
-   `--config`: Specifies the path to the config.json file.

With these options, you can customize and adjust scanning operations according to your needs.

Multi Sonar Scanner is an open-source tool that can be easily customized. You can examine the source code and use it in a special way for your own projects. Furthermore, you can use it as much as you want without paying any licensing fees.

## Important reminder
To use Multi Scanner, it's important to disable your project's SCM Sensor. This tool scans the top-level file without accessing the project directory directly, which can result in SonarQube ignoring certain project files.

![Screenshot 2023-03-20 021201](https://user-images.githubusercontent.com/72748666/226216190-c2b37579-419c-4e3f-bd74-8efdd50b3f65.png)

## Configuration Options

The following are the available configuration options in Multi Sonar Scanner:

#### Config Example: 
```
{
    "url": "http://localhost:9000",
    "os": "win",
    "projects": [
        {
            "project_key": "burak",
            "token": "sqp_e975bfd38a79d47e65f4a1314c299084a2e1514d1",
            "location": "./burak",
            "source": "git-remote",
            "git_url": "https://github.com/BaboUsN/English-Sentence-And-Mean-Collecter",
            "branch": "main"
        }
    ]
}


-   `url`: Specifies the URL of the SonarQube server.
-   `os`: Specifies the operating system. It can be "win", "linux", or "mac".
-   `projects`: Specifies the list of projects to be scanned.
-   `project_key`: Specifies the unique identifier of the project.
-   `token`: Specifies the authentication token for the project.
-   `location`: Specifies the location of the project files.
-   `source`: Specifies the source of the project files. It can be "git-remote" or "local".
-   `git_url`: Specifies the Git URL of the project (required if the source is "git-remote").
-   `branch`: Specifies the branch to be scanned (required if the source is "git-remote").

By customizing these configuration options, you can perform scans on various SonarQube projects with ease. `
