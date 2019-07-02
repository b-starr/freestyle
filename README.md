# A Personal Daily Budgeting App for Python Freestyle project
(Adapted from Readme.md for Robo-Advisor)
A basic daily budgeting app that tracks your income and spending per day given inputs for line items, and your monthly income.

## Prerequisites

  + Anaconda 3.7
  + Python 3.7
  + Pip
  + gspread oauth2client


## Installation

Fork this repository under your own control, then clone or download the resulting repository onto your computer. Then navigate to that repository from the command line.

```sh
cd freestyle.py
```

```sh
conda create -n freestyle python=3.7 # (first time only)
conda activate freestyle
```

## Setup

Before using or developing this application, take a moment to ensure you are an editor on [this google sheet](https://docs.google.com/spreadsheets/d/1eVf8trq0fzgapnIvy4QXyW8Ifas1x_WmlSnCWlkS7WA/edit#gid=0) 

## Usage

Run the script:

```py
python app/freestyle.py
```

### Inputs
Follow the input prompts within the program to navigate your budget. 
Please note that inputs need to be integers, without currency symbols.

This program is formatted to work in USD ($).

## [License](/LICENSE.md)

