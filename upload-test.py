import gspread

from oauth2client.service_account import ServiceAccountCredentials

# Now testing uploading info directly to the google sheet using gspread and oauth2client

scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'
         ]

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

sheet = client.open('python data input test').sheet1

othersheet = client.open('AHA Student Registration').sheet1


current_row = othersheet.row_values(2)


for i in range(2,8):
    current_row = othersheet.row_values(i)
    sheet.insert_row(current_row,i)




# updating the specified cell (1,1) or 'A1' with new text
# sheet.update([['wazzaaaaap']], 'A1')

# Getting the contents of the very first cell in the spreadsheet and printing it to the console window
# first_cell = sheet.cell(1,1)
# print(f"{first_cell}")

# Inserting new row
#email = 'testemail@abc.net'
#first = 'John'
#middle = ''
#last = 'Doe'
#phone = '(555) 555-5555'
#ourse = 'BLS'
#date = '3/4/26'
#acreg = 'YES'
#ahareg = 'YES'
#remind = 'NO'

# lines = [email, first, middle, last, phone, course, date, acreg, ahareg, remind]
#if sheet.find(lines[0]) == None:
#    sheet.insert_row(lines,2)
#else:
#    print("redundant entry! Not uploaded to sheet")

