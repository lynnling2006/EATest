# EATest

This application is built to do API testing using python script with the use of Pytest module as testing framework


## Installation

Follow below steps to prepare the environment.

__Install Python__:
```sh
This application builds based on python version 3.10.0
```
__Install Pipenv__:

After python is installed, run following command to install tool pipenv.
```sh
pip install pipenv
```
__Install other package__:

After pipenv is ready, enter into repository root folder, run following command to prepare virtual environment
```sh
pipenv install
```

## Automated tests
__To run a test, enter into repository root folder, run following command on Terminal__:
```sh
pipenv run pytest
```
After run test, test report file is in folder ./report, log files is in folder ./log.
