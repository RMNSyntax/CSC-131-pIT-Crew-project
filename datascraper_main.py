# By Rhianna Nichols Thomae, 2/11/2026
# CSC 131 Software Engineering Project - Automated Webpage Parser test

import datascraper_urlconvert as urlconvert
# import datascraper_mailbag as mailbag
import RQI_upload
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import gspread
from oauth2client.service_account import ServiceAccountCredentials

options = Options()
options.add_argument("-profile")
options.add_argument("C:/Users/Ryan/AppData/Roaming/Mozilla/Firefox/Profiles/38LpQTRD.Profile 1")
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)


def AHA_new_student(tablecells, class_date):
    sheetline = []
    course_name = ""
    fulltitle = driver.find_element(By.CLASS_NAME, "viewClass_classTitle__kzdvA").text
    if "BLS" in fulltitle:
        course_name = "BLS"
    elif "ACLS" in fulltitle:
        course_name = "ACLS"
    elif "PALS" in fulltitle:
        course_name = "PALS"

    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'
             ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)

    # sheet = client.open('AHA Registration TEST COPY').sheet1
    full = client.open_by_key('1k309GvE7FI9pdAJVmhrE3ha1-LFuFB96fRA2P78HOJU')
    sheet = full.worksheet("AHA Registration")
    phone = ""
    row = 2
    for i in range(0, len(tablecells) - 1, 5):

        email = tablecells[i].text
        nameplusnumber = tablecells[i + 1].text

        registered = tablecells[i + 2].text
        enrolled_by = tablecells[i + 3].text

        # Theoretically: "John May Dwyer\n(245) 306-2845"
        a = nameplusnumber.find(" ")
        fname = nameplusnumber[0:a]
        c = nameplusnumber.find("\n")
        if c != -1:
            phone = nameplusnumber[c + 4:]
        b = nameplusnumber[a + 1:c].find(" ")
        mname = ""
        if b != -1:
            mname = nameplusnumber[a + 1:b]
            lname = nameplusnumber[b + 1:c]
        else:
            lname = nameplusnumber[a + 1:c]

        studentinfo = ["", "", email, fname, mname, lname, email, "", "", "", "", "", "", "", "", "", "", "", phone,
                       course_name, class_date, "", "YES"]
        sheet.insert_row(studentinfo, row)
        row += 1


def acuity_new_student(course_name, fullname, phone, email, classdate, location):
    a = fullname.find(" ")
    fname = fullname[0:a]
    lname = fullname[a + 1:]

    lc = location.find(",")
    locformat = location[lc + 2:] + " " + location[0:lc]

    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'
             ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)

    # sheet = client.open('AHA Registration TEST COPY').sheet1
    full = client.open_by_key('1k309GvE7FI9pdAJVmhrE3ha1-LFuFB96fRA2P78HOJU')
    sheet = full.worksheet("AHA Registration")

    studentinfo = ["", locformat, email, fname, "", lname, email, "", "", "", "", "", "", "", "", "", "", "", phone,
                   course_name, classdate, "YES", ""]
    sheet.insert_row(studentinfo, 2)


def main():

    with open("Acuity_email.txt", 'r') as af:
        datestr = ""
        locstr = ""
        namestr = ""
        coursestr = ""
        phonestr = ""
        emailstr = ""
        for line in af:
            if "Subject: " in line:
                if "BLS" in line:
                    coursestr = "BLS"
                elif "ACLS" in line:
                    coursestr = "ACLS"
                elif "PALS" in line:
                    coursestr = "PALS"
                d = line.find(",")
                dend = line[d + 1:].find(",")
                dend += d + 7
                datestr = line[d + 2:dend]
            elif "Name:" in line:
                namestr = line[6:-1]
            elif "Phone:" in line:
                phonestr = line[7:-1]
            elif "Email:" in line:
                emailstr = line[7:-1]
            elif line[0:4].isnumeric():
                l2 = line.rfind(" ")
                l1sub = line.rfind(",")
                l1 = line[:l1sub].rfind(",")
                locstr = line[l1 + 2:l2]

        print(f'New Aquity student: {namestr}\n Uploading info to Combined AHA sheet...')
        acuity_new_student(coursestr, namestr, phonestr, emailstr, datestr, locstr)
        print('Done.\n')
    af.close()


    with open("email.txt", 'r') as f:
        for line in f:
            if "You have one or more incoming class enrollment requests" in line:
                datestr = line[-12:-2]
                break
    date = urlconvert.dateparser(datestr)
    mm = date[0]
    dd = date[1]
    yy = date[2]
    f.close()
    newurl = urlconvert.urlmaker(mm, dd, yy)
    driver.get(newurl)
    time.sleep(2)

    # okay it actually works without any tricks or secrets now

    tabledata = driver.find_elements(By.TAG_NAME, "td")
    idx = 3
    for i in range(3, len(tabledata) - 1, 6):
        d = tabledata[i]
        if f'0{mm}-{dd}-{yy}' in d.text:
            newbutton = tabledata[i + 2].find_element(By.TAG_NAME, "a")
            newbutton.click()
            time.sleep(0.3)
            dropdown = tabledata[i + 2].find_element(By.TAG_NAME, "ul")
            view = dropdown.find_element(By.CSS_SELECTOR, "[aria-label='View']")
            view.click()
            break
    time.sleep(2)
    buttons = driver.find_elements(By.CSS_SELECTOR, "[title='Accept']")
    for idx in buttons:
        idx.click()
        time.sleep(0.1)
        popup = driver.find_element(By.ID, "InviteItem")
        accept = popup.find_element(By.CSS_SELECTOR, "[aria-label='Accept']")
        accept.click()

    tabledata = ""
    tabledata = driver.find_elements(By.TAG_NAME, "td")
    if tabledata:
        print(f'New students found. Uploading info to Combined AHA Sheet...')
        AHA_new_student(tablecells=tabledata, class_date=datestr)
        print('Done.\n')

    driver.close()
    RQI_upload.sheetgrab()

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
