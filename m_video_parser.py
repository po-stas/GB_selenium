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

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path=r"/Users/postas/PycharmProjects/GB_selenium/venv/chromedriver",
                          options=options)
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
            collection.insert_one({'title': title_text, 'link': link, 'price': price})

    # Next Page
    try:
        button = driver.find_element_by_class_name('sel-hits-button-next')
        class_name = button.get_attribute('class')
        if 'disabled' in class_name:
            break
        button.click()
        time.sleep(2)

    except Exception:
        break

driver.quit()

# Check results
for item in db['mvideo'].find({}):
    pprint(item)


# Result example
# /Users/postas/PycharmProjects/GB_selenium/venv/bin/python /Users/postas/PycharmProjects/GB_selenium/GB_selenium/m_video_parser.py
# {'_id': ObjectId('5e4137e56ca90c5bee27373a'),
#  'link': 'https://www.mvideo.ru/products/noutbuk-asus-f509fl-ej214t-30046823',
#  'price': '34 990¤',
#  'title': 'Ноутбук ASUS F509FL-EJ214T'}
# {'_id': ObjectId('5e4137e56ca90c5bee27373b'),
#  'link': 'https://www.mvideo.ru/products/elektrobritva-philips-s3133-51-20063823',
#  'price': '3 990¤',
#  'title': 'Электробритва Philips S3133/51'}
# {'_id': ObjectId('5e4137e66ca90c5bee27373c'),
#  'link': 'https://www.mvideo.ru/products/smartfon-redmi-note-8t-64gb-moonshadow-grey-30046729',
#  'price': '15 990¤',
#  'title': 'Смартфон Redmi Note 8T 64GB Moonshadow Grey'}
# {'_id': ObjectId('5e4137e66ca90c5bee27373d'),
#  'link': 'https://www.mvideo.ru/products/holodilnik-bosch-serie-4-kgn39vw1mr-20040410',
#  'price': '31 990¤',
#  'title': 'Холодильник Bosch Serie | 4 KGN39VW1MR'}
# {'_id': ObjectId('5e4137e86ca90c5bee27373e'),
#  'link': 'https://www.mvideo.ru/products/smartfon-oppo-a5-2020-dazzling-white-cph1931-30045963',
#  'price': '10 990¤',
#  'title': 'Смартфон OPPO A5 2020 Dazzling White (CPH1931)'}
# {'_id': ObjectId('5e4137e86ca90c5bee27373f'),
#  'link': 'https://www.mvideo.ru/products/stiralnaya-mashina-uzkaya-indesit-bwsd-61051-1-20036060',
#  'price': '13 990¤',
#  'title': 'Стиральная машина узкая Indesit BWSD 61051 1'}
# {'_id': ObjectId('5e4137e86ca90c5bee273740'),
#  'link': 'https://www.mvideo.ru/products/smartfon-oppo-a5-2020-mirror-black-cph1931-30045964',
#  'price': '10 990¤',
#  'title': 'Смартфон OPPO A5 2020 Mirror Black (CPH1931)'}
# {'_id': ObjectId('5e4137e86ca90c5bee273741'),
#  'link': 'https://www.mvideo.ru/products/kofemashina-kapsulnogo-tipa-krups-nescafe-dolce-gusto-lumio-kp130110-20040153',
#  'price': '5 990¤',
#  'title': 'Кофемашина капсульного типа KRUPS NESCAFE DOLCE GUSTO LUMIO '
#           'KP130110'}
# {'_id': ObjectId('5e4137ea6ca90c5bee273742'),
#  'link': 'https://www.mvideo.ru/products/smartfon-oppo-a9-2020-marine-green-cph1941-30045965',
#  'price': '17 990¤',
#  'title': 'Смартфон OPPO A9 2020 Marine Green (CPH1941)'}
# {'_id': ObjectId('5e4137ea6ca90c5bee273743'),
#  'link': 'https://www.mvideo.ru/products/pylesos-ruchnoi-handstick-tefal-air-force-extreme-silence-ty8995ro-20055627',
#  'price': '12 990¤',
#  'title': 'Пылесос ручной (handstick) Tefal Air Force Extreme Silence TY8995RO'}
# {'_id': ObjectId('5e4137ea6ca90c5bee273744'),
#  'link': 'https://www.mvideo.ru/products/lazernoe-mfu-hp-laserjet-pro-mfp-m28a-30032665',
#  'price': '8 990¤',
#  'title': 'Лазерное МФУ HP LaserJet Pro MFP M28a'}
# {'_id': ObjectId('5e4137ea6ca90c5bee273745'),
#  'link': 'https://www.mvideo.ru/products/muzykalnyi-centr-mini-telefunken-tf-ps2201-black-10020899',
#  'price': '6 990¤',
#  'title': 'Музыкальный центр Mini Telefunken TF-PS2201 Black'}
# {'_id': ObjectId('5e4137ed6ca90c5bee273746'),
#  'link': 'https://www.mvideo.ru/products/3d-ruchka-qub-qbcp-10-pink-3dpenqbpk-30046287',
#  'price': '1 590¤',
#  'title': '3D-ручка QUB QBCP-10 Pink (3DPENQBPK)'}
# {'_id': ObjectId('5e4137ed6ca90c5bee273747'),
#  'link': 'https://www.mvideo.ru/products/televizor-samsung-ue43nu7097u-10021089',
#  'price': '26 990¤',
#  'title': 'Телевизор Samsung UE43NU7097U'}
# {'_id': ObjectId('5e4137ed6ca90c5bee273748'),
#  'link': 'https://www.mvideo.ru/products/3d-ruchka-qub-qbcp-10-light-blue-3dpenqbbl-30046286',
#  'price': '1 590¤',
#  'title': '3D-ручка QUB QBCP-10 Light Blue (3DPENQBBL)'}
# {'_id': ObjectId('5e4137ed6ca90c5bee273749'),
#  'link': 'https://www.mvideo.ru/products/pylesos-s-pylesbornikom-tefal-x-trem-power-tw6851ea-20063372',
#  'price': '9 990¤',
#  'title': 'Пылесос с пылесборником Tefal X-trem power TW6851EA'}
# {'_id': ObjectId('5e4137ef6ca90c5bee27374a'),
#  'link': 'https://www.mvideo.ru/products/fotoapparat-momentalnoi-pechati-fujifilm-instax-mini-9-clear-purple-10021665',
#  'price': '5 490¤',
#  'title': 'Фотоаппарат моментальной печати Fujifilm INSTAX MINI 9 CLEAR PURPLE'}
# {'_id': ObjectId('5e4137ef6ca90c5bee27374b'),
#  'link': 'https://www.mvideo.ru/products/kofevarka-rozhkovogo-tipa-krups-opio-xp320830-20056837',
#  'price': '8 990¤',
#  'title': 'Кофеварка рожкового типа Krups Opio XP320830'}
# {'_id': ObjectId('5e4137ef6ca90c5bee27374c'),
#  'link': 'https://www.mvideo.ru/products/besprovodnaya-akustika-jbl-flip-5-red-10022016',
#  'price': '5 990¤',
#  'title': 'Беспроводная акустика JBL Flip 5 Red'}
# {'_id': ObjectId('5e4137ef6ca90c5bee27374d'),
#  'link': 'https://www.mvideo.ru/products/parovaya-shvabra-tefal-steam-mop-vp6555rh-20042832',
#  'price': '7 990¤',
#  'title': 'Паровая швабра Tefal Steam Mop VP6555RH'}
#
# Process finished with exit code 0
