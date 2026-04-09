# By Rhianna Nichols Thomae, 2/11/2026
# CSC 131 Software Engineering Project - Automated Webpage Parser test
import subprocess

from bs4 import BeautifulSoup
import urlconvert
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import os.path
# from selenium.webdriver.common.virtual_authenticator import VirtualAuthenticatorOptions
# from playwright.sync_api import sync_playwright


import gspread
from oauth2client.service_account import ServiceAccountCredentials

options = Options()
options.add_argument("-profile")
options.add_argument("C:/Users/Ryan/AppData/Roaming/Mozilla/Firefox/Profiles/38LpQTRD.Profile 1")
# options.add_argument("--headless")
driver = webdriver.Firefox(options=options)


def new_student(tablecells,class_date):
    # nonfunctioning code atm, uses pseudocode/placeholder element strings
    sheetline = []
    course_name = ""
    fulltitle = driver.find_element(By.CLASS_NAME,"viewClass_classTitle__kzdvA")
    if "BLS" in fulltitle.text:
        course_name = "BLS"
    elif "ACLS" in fulltitle.text:
        course_name = "ACLS"




    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'
             ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)

    sheet = client.open('AHA Registration TEST COPY').sheet1
    phone = ""
    row = 2
    for i in range(0, len(tablecells)-1, 5):

        email = tablecells[i].text
        nameplusnumber = tablecells[i+1].text

        registered = tablecells[i+2].text
        enrolled_by = tablecells[i+3].text
        a = nameplusnumber.find(" ")
        fname = nameplusnumber[0:a]
        b = nameplusnumber.find("\n")
        if b != -1:
            lname = nameplusnumber[a+1:b]
            phone = nameplusnumber[b+4:]
        else:
            lname = nameplusnumber[a+1:]

        studentinfo = [email, fname, "", lname, phone, course_name, class_date, "", "YES"]
        sheet.insert_row(studentinfo, row)
        row += 1



def main():
    #driver.get("https://atlas.heart.org/dashboard")
    datestr = ""
    with open("email.txt", 'r') as f:
        for line in f:
            if "You have one or more incoming class enrollment requests" in line:
                datestr = line[-12:-2]
                break
    date = urlconvert.dateparser(datestr)
    mm = date[0]
    dd = date[1]
    yy = date[2]
    newurl = urlconvert.urlmaker(mm, dd, yy)
    driver.get(newurl)
    time.sleep(2)

    # okay it actually works without any tricks or secrets now

    tabledata = driver.find_elements(By.TAG_NAME, "td")
    idx = 3


    for i in range(3, len(tabledata)-1, 6):
        d = tabledata[i]
        if f'0{mm}-{dd}-{yy}' in d.text:
            newbutton = tabledata[i+2].find_element(By.TAG_NAME, "a")
            newbutton.click()
            time.sleep(0.3)
            dropdown = tabledata[i+2].find_element(By.TAG_NAME, "ul")
            view = dropdown.find_element(By.CSS_SELECTOR, "[aria-label='View']")
            view.click()
            break
    time.sleep(2)
    tabledata = ""

    tabledata = driver.find_elements(By.TAG_NAME, "td")
    new_student(tablecells=tabledata,class_date=datestr)

    driver.close()



    f = open("webdata.txt", 'w')
    lines = []
    for line in lines:
        f.write(line)
        f.write('\n')

    f.close()


    # Automated opening of the output text file. Runs a powershell command to just open webdata after writing to it.
    # This only works on windows machines!!! Will need to edit for linux/Mac
    # subprocess.run(["powershell", 'Invoke-Item -path "webdata.txt"'], shell=True)
    return


main()


# Selenium Login Test
"""
url = f"https://ahasso.heart.org/login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fscope%3Dopenid%2520profile%2520email%26response_type%3Dcode%26code_challenge_method%3DS256%26redirect_uri%3Dhttps%253A%252F%252Fatlas.heart.org%252Flocation%26state%3D2afa29aa-0747-46e9-afed-a17e6056e106%26client_id%3DAHA-ATLAS-PROD%26code_challenge%3DF04-q4p2L15wYutR8OKGPdXmOTlYP6Ik_rBtJ8VnepU"
driver.get(url)
time.sleep(2)
email = driver.find_element(By.ID, "Email")
email.send_keys("Sacstatecpr@outlook.com")
passw = driver.find_element(By.ID, "Password")
passw.send_keys("ssCPR123*")
signin = driver.find_element(By.ID, "btnSignIn")
signin.click()
time.sleep(5)
signin = driver.find_element(By.CLASS_NAME, "")
signin.click()
"""

# Playwright Login Test
"""
Just Kidding, I never got to do a playwright login test because it still won't install!!! Yippee!!!!
"""

