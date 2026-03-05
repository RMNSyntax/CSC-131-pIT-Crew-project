import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Now testing uploading info directly to the google sheet using gspread and oauth2client

scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json',scope)
client = gspread.authorize(credentials)

sheet = client.open('python data input test').sheet1

# Updating the first column, second row (A2) with a given string
sheet.update([['Hello world!! this is the second row of the first column!']], 'A2')

# Getting the contents of the very first cell in the spreadsheet and printing it to the console window
first_cell = sheet.cell(1,1)
print(f"First cell of Data: {first_cell}")