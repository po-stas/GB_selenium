from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as exc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pymongo import MongoClient
from pprint import pprint
import time

client = MongoClient('localhost', 27017)
db = client['selenium_DB']
collection = db['mvideo']

driver = webdriver.Chrome(executable_path=r"/Users/postas/PycharmProjects/GB_selenium/venv/chromedriver")
driver.get('https://www.mvideo.ru/buy-now')

while True:
    # Wait for page to be ready
    items_container = WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'accessories-product-list')))
    items_list = items_container.find_elements_by_class_name('gallery-list-item')
    for item in items_list:
        title = item.find_element_by_class_name('sel-product-tile-title')
        title_text = title.text
        if title.text:
            link = title.get_attribute('href')
            price = item.find_element_by_class_name('c-pdp-price__current').text
            print(f'{title_text}: {link}, {price}')

    # Next Page
    try:
        button = driver.find_element_by_class_name('sel-hits-button-next')
        style = button.get_attribute('style')
        if 'none' in style:
            print('End of List')
            break
        button.click()
        time.sleep(2)

    except Exception:
        print('End of List')
        break
