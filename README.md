# Power Aid 

## Project Description
The purpose of this project is to provide with data about estimations, consumption and production of electrical energy to everyone that may be interested. Moreover, it is made to be used by third parties through the API. 

This repository hosts the [Software Engineering](https://courses.softlab.ntua.gr/softeng/2019b) assignment for NTUA Course "Software Engineering" (Fall 2019 - Winter 2020).
The application is developed using the Flask web application framework and python3.6.

## :mens: About the team
The project was created by the team "3 of a kind" which consists of the members:
* Salpea Natalia ( AM:03116083, natalia.e.salpea@gmail.com)
* Kostopanagiotis Panagiotis ( AM: 03115196, panagiotis.kostopanagiotis@gmail.com)
* Mavrogeorgis Konstantinos ( AM: 03115104, blackgeorge1997@gmail.com)

## :wrench: How to setup the application
To start the app you need to execute a make command 
```bash
make all
```
while in the /back-end directory. In there exists the Makefile file that contains the make targets. You can execute each specific target individually by running make install (to install all requirements/dependencies), make files (to download needed files for the database), make db (to create the datapage and load it with data), make run
(to start the server), make test (to run unit and functional tests), make clean (to delete the downloaded files) respectively.
```bash
make install
make files
make db
make run
make test
make clean
```
When executing 
```bash
make all
``` 
make stops at the run target so make test and make clean need to be executed manually as stated above.
To set up the Command Line Interface you need to execute a make command while in the cli-client/ directory
```bash
make all
```
or execute each target individually by running make install (to install requirements/dependencies) or make test (to run unit and functional tests).
```bash
make install
make test
```
## :fire: How to use the application
Once the server is up and running you can use the CLI while in the cli-client/ directory by executing commands of this format:
```bash
python3 cli.py energy_group001 scope --options
```
The scopes and their options can be seen in the matrix below:
| Scope                        	| Options                                                                                	|
|------------------------------	|----------------------------------------------------------------------------------------	|
| HealthCheck                  	|            -                                                                           	|
| Reset                        	|            -                                                                           	|
| Login                        	| --username --passw                                                                     	|
| Logout                       	|            -                                                                           	|
| ActualTotalLoad              	| --area --timeres --date or --month or--year                                            	|
| AggregatedGeneration PerType 	| --area --timeres --productiontype --date or--month or--year                            	|
|  DayAheadTotalLoadForecast  	| --area --timeres --date or--month or--year                                              |
| ActualvsForecast             	| --area --timeres --date or--month or --year                                             |
| Admin                        	|  --newuser [--passw --email --quota] --moduser [--passw --email --quota] --userstatus  	|

The permitted values for each option can be seen below:

| Options          	| Permitted values                       	|
|------------------	|----------------------------------------	|
| --timeres        	| PT15M or PT30M or PT60M                	|
| --date           	| YYYY-MM-DD                             	|
| --month          	| YYYY-MM                                	|
| --year           	| YYYY                                   	|
| --format         	| csv or json(default)                   	|
| --newuser        	| username(alphanumeric)                 	|
| --moduser        	| username(alphanumeric)                 	|
| --passw          	| anything != space                    	  |
| --email          	| email address                          	|
| --quota          	| any number                             	|
| --userstatus     	| username(alphanumeric)                 	|
| --area           	| anything from the AreaName column(db)  	|
| --productiontype 	| anything from the ProductionTypes column|
## Tecnologies Used
### Back-end
* Python3.6
* Flask
* MySQLv14.14
* Unittest

### Cli front-end
* Python3.6
* Click
* Unittest
