# Specify Command Line Export Utility
## Building exports for Specify-Hosted Web Portals

Parameters and arguments of the `ExpCmdLine` utility are as follows:

| Parameter | Argument                                                                 | Required                       |
|-----------|--------------------------------------------------------------------------|--------------------------------|
| -u        | The username of a (manager-level) Specify user                          | Yes                            |
| -p        | The user’s password                                                      | Yes                            |
| -d        | The database name                                                        | Yes                            |
| -m        | The name of the data mapping (contained within the Specify database)    | Yes                            |
| -a        | The action to be performed. Options: "Update", "ExportToTabDelim", "ExportForWebPortal" | Yes                            |
| -l        | The name of the log file                                                | No, defaults to `stdout`         |
| -h        | IP name or address of the MySQL database server                         | No, defaults to `localhost`      |
| -o        | The name of the output file                                             | No                             |
| -w        | Path to: “../Specify” installation directory                             | Yes                            |
