from dotenv import load_dotenv
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import time

load_dotenv()

DOCUMENT_ID = "1eVf8trq0fzgapnIvy4QXyW8Ifas1x_WmlSnCWlkS7WA" #os.environ.get("GOOGLE_SHEET_ID", "OOPS")
SHEET_NAME = os.environ.get("SHEET_NAME", "Budget")


#NEED TO CREATE GOOGLE_SHEET_ID VARIABLE
google_sheet_id = "1eVf8trq0fzgapnIvy4QXyW8Ifas1x_WmlSnCWlkS7WA"


#
# AUTHORIZATION
#

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

monthly_budget = input ("Input your monthly salary less taxes and savings: ")
days_of_month = input ("How many days are there this month?: ")
daily_budget = int(monthly_budget) / int(days_of_month)
print(f"Your Daily Budget is: {to_usd(float(daily_budget))}")
# print(f"RECENT LOW: {to_usd(float(recent_low))}")

print()
print("Next, you'll need to enter Income or Expenses. Please enter each line item without a currency symbol.")
print()
income_or_expense = input ("Would you like to add an expense or income? Please Type Expense or Income: ")

expense_cat = input("Input your Income/Expense Category: ")

expense_val = input("How much did you spend/earn (please exclude currency sign): ")
#print("You've input the expense: ",expense_cat, "for $", expense_val)  
print("-------------------------------------------------------------")

#if (income_or_expense == "Income"):
#    expense_val = (expense_val * -1)
#else:
#    expense_val = expense_val

#def convert_income()
#    expense_val * -1
#income_val = 

print("You've added {} to the budget for ${}".format(expense_cat,expense_val)) #Help from Anson Wang, a friend outside of class

#while True:
#        expense = input("Please input an expense for today: ")
#        if not expense.isalpha(): # STORE THE INPUT AS A VARIABLE?
#            print("Please try again.")
#        else:
#            break
#



# DAILY SUMMARY OUTPUT
#print("-------------------------------------------------------------")
#print(doc.title) 
#print("-----------------")

sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>

rows = sheet.get_all_records() #> <class 'list'>

#PRINT ALL ROWS
#for row in rows:
#    print(row) #> <class 'dict'>
#
#
# WRITE VALUES TO SHEET
#

next_id = len(rows) + 1 # TODO: should change this to be one greater than the current maximum id value

next_object = {
    "Expense Number": f"Expense # {next_id}",
    "Category": expense_cat,
    "cost": float(expense_val),

    #"department": "snacks",
    #"price": 4.99,
    #"availability_date": "2019-01-01"
}

next_row = list(next_object.values()) #> [13, 'Product 13', 'snacks', 4.99, '2019-01-01']

next_row_number = len(rows) + 2 # number of records, plus a header row, plus one

response = sheet.insert_row(next_row, next_row_number)
total_budget = sheet.cell(1, 5).value
budget_left = float(daily_budget)- float(total_budget)

print("-------------------------------------------------------------")
print("-------------------------------------------------------------")
print(f"You have {to_usd(float(budget_left))} of your budget left today.")
#print(float(daily_budget)- float(total_budget))
# print(f"RECENT LOW: {to_usd(float(recent_low))}")
print()
print("To add another line item, please re-run the program.")
print("-------------------------------------------------------------")

#print("-----------------")
#print("NEW RECORD:")
#print(next_row)
#print("-----------------")

#SUM UP A COLUMN? NOT WORKING (ANSON)
#values_list = sheet.col_values(3)
#print(sum(values_list))

#print("RESPONSE:")
#print(type(response)) #> dict
#print(response) #> {'spreadsheetId': '___', 'updatedRange': '___', 'updatedRows': 1, 'updatedColumns': 5, 'updatedCells': 5}