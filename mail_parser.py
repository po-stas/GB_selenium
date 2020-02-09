from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as exc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


email = 's_pologrudov'
password = 'Ufhvjybzlei666'
driver = webdriver.Chrome(executable_path=r"/Users/postas/PycharmProjects/GB_selenium/venv/chromedriver")
driver.get('https://mail.ru')

login_field = driver.find_element_by_id('mailbox:login')
login_field.send_keys(email)
enter_password = driver.find_element(By.XPATH, "//input[@value='Ввести пароль']")
enter_password.click()

# Wait for element will be ready
# while True:
#     password_field = driver.find_element_by_id('mailbox:password')
#     try:
#         password_field.send_keys(password)
#         break
#     except exc.ElementNotInteractableException:
#         pass

# Refactor via WebDriverWait
password_field = WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.ID, 'mailbox:password')))
password_field.send_keys(password)
enter_password.click()

# Wait for page will be ready
letters_container = WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'dataset__items')))
letters_list = letters_container.find_elements_by_class_name('js-letter-list-item')

letters = []
for letter in letters_list:
    correspondent = letter.find_element_by_class_name('ll-crpt').text
    subject = letter.find_element_by_class_name('llc__subject').text
    snippet = letter.find_element_by_class_name('ll-sp__normal').text
    date = letter.find_element_by_class_name('llc__item_date').text
    link = letter.get_attribute('href')
    letter_dic = {'corr': correspondent, 'sub': subject, 'date': date, 'snippet': snippet, 'link': link}
    letters.append(letter_dic)

# Go inside for get texts
for letter in letters:
    driver.get(letter['link'])
    letter_body = WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'letter-body__body-content')))
    letter['text'] = letter_body.text

    print(f'{letter["corr"]}: {letter["sub"]} - {letter["date"]}...{letter["text"]}')







