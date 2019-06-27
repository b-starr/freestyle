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


# DAILY SUMMARY OUTPUT
print("-----------------")
print("SPREADSHEET:", doc.title) 
print("-----------------")

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
    "item number": next_id,
    "cost": f"Product {next_id}",
    "department": "snacks",
    "price": 4.99,
    "availability_date": "2019-01-01"
}

next_row = list(next_object.values()) #> [13, 'Product 13', 'snacks', 4.99, '2019-01-01']

next_row_number = len(rows) + 2 # number of records, plus a header row, plus one

response = sheet.insert_row(next_row, next_row_number)

print("-----------------")
print("NEW RECORD:")
print(next_row)
print("-----------------")


#print("RESPONSE:")
#print(type(response)) #> dict
#print(response) #> {'spreadsheetId': '___', 'updatedRange': '___', 'updatedRows': 1, 'updatedColumns': 5, 'updatedCells': 5}