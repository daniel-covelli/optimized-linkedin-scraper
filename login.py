import time
import pickle
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

email = ''
password = ''

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Ffeed%2F%3Ftrk%3Dguest_homepage-basic_nav-header-signin%252F&fromSignIn=true&trk=cold_join_sign_in")

time.sleep(1.5)
username = driver.find_element_by_id('username')
username.send_keys(email)

password = driver.find_element_by_id('password')
password.send_keys(password)

time.sleep(1.5)
driver.find_element_by_class_name('login__form_action_container').click()

time.sleep(1.5)
pickle.dump(driver.get_cookies(), open("PremiumCredentials.pkl","wb"))
