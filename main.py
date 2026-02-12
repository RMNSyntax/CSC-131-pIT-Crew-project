# By Rhianna Nichols Thomae, 2/11/2026
# CSC 131 Software Engineering Project - Automated Webpage Parser test
import subprocess
import sys
import pkg_resources
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def install_dependencies():
    required = {'bs4', 'selenium'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])


def main():
    install_dependencies()
    # Below is a working demo for an automated browser opening the AHA website and reading page text just like a user.
    # Selenium digs through the javascript for the actual html/css, then Beautifulsoup's parser makes it readable.
    # Both are free to use. Will find ways to package these in with the final product plus their licenses

    options = webdriver.FirefoxOptions()
    # "--headless" mode operates the browser without opening a visible browser window. Commented out so we can test
    # This way the client doesn't see windows popping up any time a new student is added to the roster
    # options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)

    driver.get("https://atlas.heart.org/")
    time.sleep(2)

    # Because Selenium looks for webpage elements by specific identifiable traits, sometimes there's multiple results,
    # For now I hardcode in the exact item i want to display the subtitle underneath the big banner
    # It's a hack but it works + it proves we can find any data in a webpage that we need and extract it
    # TODO: To extract student info from the AHA site, we need to automate logging in securely without errors.

    banner = driver.find_element(By.TAG_NAME, "h1")
    bannertext = BeautifulSoup(banner.get_attribute("innerHTML"), 'html.parser')
    print(bannertext.get_text())                                        # Print to console just to verify it's working

    popups = driver.find_elements(By.TAG_NAME, "p")
    popup = popups.__getitem__(1)
    popuptext = BeautifulSoup(popup.get_attribute("innerHTML"), 'html.parser')
    print(popuptext.get_text())                                         # Ditto

    # Then the extracted webpage data is stored as plain text in a .txt file.
    # If it can be stored in a .txt it can be spat back out into a spreadsheet without too much effort, right?
    # TODO: test that assumption???

    f = open("webdata.txt", 'w')
    lines = [bannertext.get_text(),popuptext.get_text()]
    for line in lines:
        f.write(line)
        f.write('\n')

    f.close()

    # Automated opening of the output text file. Runs a powershell command to just open webdata after writing to it.
    # This only works on windows machines!!! Will need to edit for linux/Mac
    subprocess.run(["powershell", 'Invoke-Item -path "webdata.txt"'], shell=True)
    return

main()


# Bunch of early tests to see if any of this actually worked. Found a way to enter username/password info and click
# the login button, but it gives a "ssoverifier missing" error and doesn't load the actual user dashboard or profile.
# TODO: Emmanuel and Irving, can you find a way to fix this?
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
time.sleep(2)
signin = driver.find_element(By.XPATH, "//input[@button class='btn btn-link Header_disableSignIn__jFG_h']")
signin.click()




soup = BeautifulSoup("<p>Some <b>bad <i>HTML!!!", 'html.parser')
print(soup.get_text())


res = requests.get('https://atlas.heart.org/organisation/view-class?id=20008252&applyTsFilter=false&isClassesTeach=true&isNavigated=true')
soup = BeautifulSoup(res.content, 'html.parser')
print(soup.prettify())

content = soup.find('div', class_='article--viewer_content')
if content:
    for para in content.find_all('p'):
        print(para.text.strip())
else:
    print("No article content found.")
"""


