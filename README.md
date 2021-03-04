# Capstone2021

## Installing Python 3.8

## Installing MySQL

## Installing Poetry

### Windows:

Open Powershell as administrator and run the following command: (Search for Powershell, right-click and select "Run as Administrator")
``
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
``

### MacOSX or Linux

Open Terminal:
``
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
``

## Starting MySQL Database

## Running Visualization WebApp

### Windows

Open Powershell as administrator and navigate to VinfenClientPhoneTool directory and run:
``
poetry install
poetry shell
bokeh serve --show vinfenclientphonetool/myapp.py
``

### MacOSX or Linux

Open Terminal:
``
poetry install
poetry shell
bokeh serve --show vinfenclientphonetool/myapp.py
``

## Populating MySQL Database
