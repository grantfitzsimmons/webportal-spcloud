# Specify Command Line Export Utility

The Specify Command Line Data Export Program (`ExpCmdLine`) is a software tool
which enables database administrators to automate the process of producing exported
collection records to update a Specify Web Portal, or to create tab-delimited text files of
exported collection data for other uses.

Specify has a flexible mechanism for identifying which data fields will be included in an
exported data file. 

Setting up a pipeline for exporting data includes a few steps and
some additional software tools. The **Specify Schema Mapper** is an embedded tool in Specify 6 
accessible from the “System” menu for manager-level users. It enables the creation of
an 'Schema Mapping', which is a custom mapping between the data fields used in a
Specify database and the data concepts one wishes to include and populate in an export
file. 

The **Specify Data Exporter** application, a separate program included with Specify, is
an interactive tool which uses an Export Data Map to copy the data in the mapped fields
to a single table within the Specify database. 

This flat table in MySQL is an
‘index’ or ‘cache’ copy of the export data. Once an internal cache is created, the Data
Exporter can either export the data as a flat, tab-delimited, text file (e.g. for GBIF’s IPT
software to create a DarwinCore Archive data package), or data can be exported and
associated configuration files packaged inside of a .zip file which can be saved and used
for updating a Specify Web Portal.

The Command Line Data Export Program, included in the Specify installation, is
similar in function to the Specify Data Exporter; it uses Export Data Maps to update a
flat table internal cache and can also export that data to a tab-delimited test file or to a
Web Portal zip package. The main difference between the two applications is that the
Data Exporter is interactive whereas the Command Line Data Exporter can perform
these actions in a “headless” environment which can be scripted.

## Read Me First

The first time a Schema Mapping is made with the Schema Mapper function, Specify’s
interactive Data Exporter application (not `ExpCmdLine`) must be used to create the
initial database cache copy and to export the zip file package which is used by the Specify
Web Portal. 

After the first export, ExpCmdLine replaces the need to use the interactive Specify Data
Exporter application for pushing recurring data updates from a Specify database. Web
Portal updates can then be automated by using ExpCmdLine in a scripted, scheduled
job from a server account.

**Note:** If the Specify data mapping is changed because the Specify Schema Mapper was used
to add/remove/shift/change mapped concepts, or to change titles for output fields, or to change record selection conditions, then the internal, flat table, MySQL cache or
index must be rebuilt using the Specify Data Exporter tool (not ExpCmdLine ). If an
internal cache rebuild is necessary ExpCmdLine will fail and not complete a Portal
update. After a rebuild of the internal cache, this tool can then again be used for
scripting recurring updates to update the internal cache and separately to export the
Web Portal zip package by using the appropriate argument to the –a parameter.

**A Specify manager-level user account is required to use this tool.**

## Prerequisites

- Java JRE 8 
    - On Ubuntu, you can run `sudo apt install openjdk-8-jdk`
- MariaDB 
    - Run `sudo apt install libmariadb-dev` to install the MariaDB client library
    - After this, run `pip3 install mariadb` to install the MariaDB Python connector
- Python 3.10 or later

# Using This Utility

_These steps assume you are using a Linux or macOS system._

After cloning this repository, you must then navigate to the `specify/bin` directory and run the following command to make the `ExpCmdLine` utility executable:

```bash
chmod +x ExpCmdLine
```

You will need to enter a Python virtual environment by running the following command inside the `/webportal-spcloud/specify/bin` directory:

```bash
source source venv/bin/activate
```

Once done, you can find which export mappings are available in the database by running the `FindAvailableExportMappings.py` script.

```bash
python ../../FindAvailableExportMappings.py
```

You can build a command to update or export data from a Specify database by running the `BuildCommand.py` script.

```bash
python ../../BuildCommand.py
```

If you encounter any issues, the logs are stored in the `specify/bin/logs` directory. You can also view the logs in the terminal you are running the commands in.

## Parameters and arguments for `ExpCmdLine`

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


If you see `java.lang.Exception: mapping must be rebuilt.`, you must first rebuild the mapping using the DataExporter tool GUI.

# BuildCommand.py

This script is used to build an export mapping in a specified database. It connects to the database, fetches the available mappings, and displays them.

## Usage

To use the script, run the following command:

```bash
python BuildCommand.py
```

The script will prompt you to enter the database name, username, password, and the IP address of the MySQL server. It will then connect to the database, fetch the available mappings, and display them.

```bash
❯ python3 ../../BuildCommand.py                                                                    Py bin at 01:08:39 PM
Enter the database name: ku_fish
Enter the username: spfishadmin
Enter the password: testuser
Enter the mapping name: DwCKUI
Enter the action (Update, ExportForWebPortal, or ExportToTabDelim): ExportForWebPortal
Enter the host name (or leave blank for localhost): 

Generated Command:
./ExpCmdLine -u "spfishadmin" -p "testuser" -d ku_fish -m "DwCKUI" -a ExportForWebPortal -l logs/ku_fish_2024-08-30_13-09-05.log -h localhost -o ku_fish_2024-08-30.txt -w ./specify
```

You can then run the generated command to perform the export. Note the syntax for running `ExpCmdLine` will depend on the operating system you are using.

```bash
❯ ./ExpCmdLine -u "spfishadmin" -p "testuser" -d ku_fish -m "DwCKUI" -a ExportForWebPortal -l logs/ku_fish_2024-08-30_13-09-05.log -h localhost -o ku_fish_2024-08-30.txt -w ./specify
```


# FindAvailableExportMappings.py

This script is used to find available export mappings in a specified database. It connects to the database, fetches the available mappings, and displays them.

## Usage

To use the script, run the following command:

```
python FindAvailableExportMappings.py
```

The script will prompt you to enter the database name, username, password, and the IP address of the MySQL server. It will then connect to the database, fetch the available mappings, and display them.

```bash
❯ python ../../FindAvailableExportMappings.py

Do you need to connect via SSH? (yes/no): no
No SSH connection will be established.
Enter the MariaDB username: root
Enter the MariaDB password: 
Enter the database name: ku_fish
Successfully connected to the database.

Schema Mappings:
Mapping Name                   Collection Name                Discipline Name
================================================================================
DwCKUIT                        KU Fish Tissue Collection      Ichthyology
DwCKUI                         KU Fish Voucher Collection     Ichthyology
Tissue web search              KU Fish Tissue Collection      Ichthyology
Voucher web search             KU Fish Voucher Collection     Ichthyology
BI portal KUI                  KU Fish Voucher Collection     Ichthyology
BI portal KUIT                 KU Fish Tissue Collection      Ichthyology
Database connection closed.  
```
