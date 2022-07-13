# EATest

This application is built to do REST API testing using python scripts with the use of Pytest module as testing framework


## Installation

following below steps to prepare the environment

__Install Python__:
```sh
version requires above 3.10.0
```
__Install Pipenv__:
after python is installed, run following command to install tool pipenv
```sh
pip install pipenv
```
__Install other package__:
after pipenv is reay, enter into repository root foler, run following command to prepare virtual environment
```sh
pipenv install
```

## Automated tests
__To run a test, enter into repository root folder, run following command on Terminal__:
```sh
pipenv run pytest
```
after test running, test report file is in folder ./report, log files is in folder ./log
