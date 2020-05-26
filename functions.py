import csv
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains

def csvwriter(dictionary, cols, currentcustomer):
    found = False
    for entry in dictionary:
        comp, name, desc, role, link = entry.items()
        if currentcustomer in comp[1]:
            found = True

    if not found:
        dictionary.append({'Company': currentcustomer, 'Name': None, 'Description': None,
                           'Role': None, 'LinkedIn URL': None})

    csv_file = str(currentcustomer) + "CTOlist.csv"

    try:
        path = Path('./Output/Archive')
        fpath = (path/csv_file).with_suffix('.csv')
        with fpath.open(mode='w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cols)
            writer.writeheader()
            for data in dictionary:
                writer.writerow(data)
    except IOError:
        print('I/O error')

def waitforclass(element, webdriver, time=10):
    elementPresent = EC.presence_of_element_located((By.CLASS_NAME, element))
    WebDriverWait(webdriver, time).until(elementPresent)

def scrape(webdriver, clickable, dictionary, currentcustomer, subdescription, tocontinue=False):
    desired_y = (clickable.size['height'] / 2) + clickable.location['y']
    window_h = webdriver.execute_script('return window.innerHeight')
    window_y = webdriver.execute_script('return window.pageYOffset')
    current_y = (window_h / 2) + window_y
    scroll_y_by = desired_y - current_y

    webdriver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
    waitforclass('search-result__info', webdriver)
    clickable.click()

    try:
        goBackButton = webdriver.find_element_by_xpath("//*[text()[contains(.,'Go back')]]")
        goBackButton.click()
        print('out of network')
        tocontinue = True
    except:
        waitforclass('pv-oc', webdriver)

        contactName = webdriver.find_element_by_css_selector('.inline.t-24').text
        contactDescription = webdriver.find_element_by_css_selector('.mt1.t-18').text
        if "Past" in subdescription:
            contactRole = contactDescription
        else:
            contactRole = subdescription
        
        contactURL = webdriver.current_url

        dictionary.append({'Company': currentcustomer, 'Name': contactName, 'Description': contactDescription,
                           'Role': contactRole, 'LinkedIn URL': contactURL})
    return tocontinue

def clickretry(webdriver):
    try:
        webdriver.find_element_by_xpath(
            "//div[@class= 'search-no-results__container']//button[contains(@class, 'artdeco-button')]").click()
        waitforclass("subline-level-1", webdriver)
    except:
        waitforclass("subline-level-1", webdriver)