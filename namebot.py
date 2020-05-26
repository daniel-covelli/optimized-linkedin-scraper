
import pandas as pd
import time
import pickle
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from functions import csvwriter
from functions import waitforclass
from functions import scrape
from functions import clickretry

# data cleaning
data = pd.read_excel('Customer List Automotive.xlsx')
customerlist = data['Unnamed: 1'].values.tolist()

# output data
csvColumns = ['Company','Name','Description', 'Role', 'LinkedIn URL']
csvDict = []

# automation variables
driver = webdriver.Chrome(ChromeDriverManager().install())

# profile button, description, and subdescription Xcode
notCompany = "//div[contains(@class, 'search-result--person')]"
profile = "//div[contains(@class,'search-result__info')]"
clickable = "//a[contains(@class, 'search-result__result-link ember-view')]"
description = "//a[contains(@class, 'search-result__result-link ember-view')]/following-sibling::p[1]"
subdescription = "//a[contains(@class, 'search-result__result-link ember-view')]/following-sibling::p[3]"

# keywords
roles = ['CTO', 'echnical', 'echnology', 'ngineer', 'afety']
antiroles = ['inacial', 'inance']

# ______________________________________________________________________________________ #

driver.get("https://www.linkedin.com/login?trk=homepage-basic_conversion-modal-signin")

time.sleep(1.5)
for cookie in pickle.load(open("./Keys/PremiumCredentials.pkl", "rb")):
    if 'expiry' in cookie:
        del cookie['expiry']
    driver.add_cookie(cookie)

driver.get("https://www.linkedin.com/")

time.sleep(1.5)
search = driver.find_element_by_id('global-nav-typeahead')
search.click()

time.sleep(1.5)
search = driver.find_element_by_class_name("search-global-typeahead__input")

for customer in customerlist:
    print('Customer: ' + str(customer))

    search.send_keys(customer + " CTO")
    time.sleep(1)
    search.send_keys(Keys.ENTER)

    customerNameVersions = [customer, customer.upper()]

    pageCount = 0
    while pageCount < 4:
        print('Page: ' + str(pageCount))

        waitforclass("subline-level-1", driver)

        driver.execute_script("window.scrollTo(0, 1080)")
        time.sleep(2)

        profiles = driver.find_elements_by_xpath(notCompany + profile + clickable)
        profileCount = range(len(profiles))

        for count in profileCount:
            print("Count: " + str(count))

            driver.execute_script("window.scrollTo(0, 1080)")
            time.sleep(.5)

            profileDescription = driver.find_elements_by_xpath(notCompany + description)
            currentProfileDescription = profileDescription[count]

            subDescription = driver.find_elements_by_xpath(notCompany + subdescription)
            try:
                currentSubDescription = subDescription[count].text
            except IndexError:
                currentSubDescription = ''

            profileClickable = driver.find_elements_by_xpath(notCompany + profile + clickable)
            currentProfileClickable = profileClickable[count]

            if any(antirole not in currentProfileDescription.text for antirole in antiroles) \
                    and any(version in currentProfileDescription.text for version in customerNameVersions) \
                    and any(role in currentProfileDescription.text for role in roles):

                outofnetwork = scrape(driver, currentProfileClickable, csvDict, customer, currentSubDescription)
                if outofnetwork:
                    continue

                print('scrapped')

                time.sleep(2)
                driver.execute_script("window.history.go(-1)")

                clickretry(driver)

            elif 'Current' in currentSubDescription \
                    and any(antirole not in currentProfileDescription.text for antirole in antiroles) \
                    and any(customerName in currentSubDescription for customerName in customerNameVersions) \
                    and any(role in currentSubDescription for role in roles):

                outofnetwork = scrape(driver, currentProfileClickable, csvDict, customer, currentSubDescription)
                if outofnetwork:
                    continue

                print('scrapped')

                time.sleep(2)
                driver.execute_script("window.history.go(-1)")

                clickretry(driver)

            else:
                print('not found')

        pageCount += 1
        driver.execute_script("window.scrollTo(0, 1080)")

        time.sleep(1)

        # if next page doesn't exist
        try:
            nextButton = driver.find_element_by_xpath("//*[text()[contains(.,'Next')]]")
            nextButton.click()
        except:
            csvwriter(csvDict, csvColumns, customer)
            break

    csvwriter(csvDict, csvColumns, customer)

    time.sleep(2)
    search.clear()


