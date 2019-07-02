from dotenv import load_dotenv
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import time
import calendar

load_dotenv()

DOCUMENT_ID = "1eVf8trq0fzgapnIvy4QXyW8Ifas1x_WmlSnCWlkS7WA" 
SHEET_NAME = os.environ.get("SHEET_NAME", "Budget")

#GOOGLE_SHEET_ID VARIABLE
google_sheet_id = "1eVf8trq0fzgapnIvy4QXyW8Ifas1x_WmlSnCWlkS7WA"

# AUTHORIZATION - help from Prof. R

CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "credentials.json")

AUTH_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
    "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)

#
# READ SHEET VALUES
#

client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>

doc = client.open_by_key(DOCUMENT_ID) #> <class 'gspread.models.Spreadsheet'>

# USER INPUTS 

def to_usd(my_price):
    return "${0:.2f}".format(my_price)

print()
print("Welcome to your daily budget! You'll be asked a series of questions to determine your budget and line items.")
print("Please make sure to enter only whole numbers and without any currency symbols.")
print("Let's get started!")
print()

# ADAPTED FROM https://stackoverflow.com/questions/48738218/python-3-create-error-if-user-input-is-not-an-integer and https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
while True:
    try:
        monthly_budget = int(input ("Input your monthly salary less taxes and savings this month: ") )
    except ValueError:
        print("Please make sure you input a valid integer.")
        continue
    else:
        break

# Adapted from https://stackoverflow.com/questions/9481136/how-to-find-number-of-days-in-the-current-month/9481305
now = datetime.datetime.now()
days_of_month = calendar.monthrange(now.year, now.month)[1]
daily_budget = int(monthly_budget) / int(days_of_month)
print()
print("-------------------------------------------------------------")
print(f"Your Daily Budget this month is: {to_usd(float(daily_budget))}")

daily_budget = int(monthly_budget) / int(days_of_month)
print("-------------------------------------------------------------")

expense_loop = True #Help from Anson Wang, friend outside of class
while (expense_loop):
    print()
    print("Next, you'll need to enter your line items (Income or Expenses). Please enter each line item without a currency symbol.") #TODO FAIL IF NOT INT
    print()

    expense_cat = input("Please enter the line item description: ")

    while True:
        try:
            expense_val = int(input("How much did you spend/earn (please exclude currency sign): "))
        except ValueError:
            print("Please make sure you input a valid integer.")
            continue
        else:
            break

    #print("You've input the expense: ",expense_cat, "for $", expense_val)  
    income_or_expense = input ("Is this line item income or expense? ") 
    if income_or_expense.startswith('i'): 
        expense_val = float(expense_val)*-1 #Help from Anson Wang
        print()
        print("Ok. We'll mark this as income for today.")
    else:
        print()
        print("Ok. We'll add this as an expense.")
    print("-------------------------------------------------------------")

    print("You've added {} to the budget for ${}".format(expense_cat,expense_val)) #Help from Anson Wang

    sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>

    rows = sheet.get_all_records() #> <class 'list'>

    # WRITE VALUES TO SHEET

    next_id = len(rows) + 1 
    next_object = {
        "Expense Number": f"Expense # {next_id}",
        "Category": expense_cat,
        "cost": float(expense_val),
    }

    next_row = list(next_object.values()) 
    next_row_number = len(rows) + 2 # number of records, plus a header row, plus one

    response = sheet.insert_row(next_row, next_row_number)
    total_budget = sheet.cell(1, 5).value
    budget_left = float(daily_budget)- float(total_budget)

    print()
    print("-------------------------------------------------------------")
    print(f"You have {to_usd(float(budget_left))} of your budget left today.")
    if budget_left < 0:
        print("You've gone over your budget today - be sure to save more tomorrow!")
    print()
    print("-------------------------------------------------------------")


    add_more = input("Would you like to add more line items? ") #Adapted from https://stackoverflow.com/questions/17953940/yes-or-no-output-python and https://github.com/burnash/gspread/issues/51
    if add_more.startswith('y'): 
        pass
    else:
      expense_loop = False
      print ("Great!")


Join = input("Would you like to reset today's budget? ") #Adapted from https://stackoverflow.com/questions/17953940/yes-or-no-output-python and https://github.com/burnash/gspread/issues/51
if Join.startswith('y'): 
    cell_list = sheet.range('A2:C20')
    for cell in cell_list:
        cell.value = ""
    sheet.update_cells(cell_list)
    print("Today's budget has been reset. Thanks!")
else:
  print ("No problem. We'll leave your budget as is.")



#
# APPENDIX - unused but useful code
#

#PRINT ALL ROWS
#for row in rows:
#    print(row) #> <class 'dict'>

#print("-----------------")
#print("NEW RECORD:")
#print(next_row)
#print("-----------------")

#print("RESPONSE:")
#print(type(response)) #> dict
#print(response) #> {'spreadsheetId': '___', 'updatedRange': '___', 'updatedRows': 1, 'updatedColumns': 5, 'updatedCells': 5}