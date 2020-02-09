from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as exc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pymongo import MongoClient
from pprint import pprint
from GB_selenium.settings import password

client = MongoClient('localhost', 27017)
db = client['selenium_DB']
collection = db['mailru']

email = 's_pologrudov'
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
    collection.insert_one(letter)

    # print(f'{letter["corr"]}: {letter["sub"]} - {letter["date"]}...{letter["text"]}')

driver.quit()

# Check Results

for letter in db['mailru'].find({}):
    pprint(letter)

# Output Example:

# /Users/postas/PycharmProjects/GB_selenium/venv/bin/python /Users/postas/PycharmProjects/GB_selenium/GB_selenium/mail_parser.py
# {'_id': ObjectId('5e3fbd7648e08b0b480d9a26'),
#  'corr': 'Почта Mail.ru',
#  'date': '8 фев',
#  'link': 'https://e.mail.ru/inbox/1:3e8f8c94adc83163:0/?back=1&afterReload=1',
#  'snippet': 'Если это не вы, измените пароль. Вход с нового устройства в '
#             'аккаунт s_pologrudov@mail.ru В аккаунт s',
#  'sub': 'Вход с нового устройства в аккаунт',
#  'text': '          Вход с нового устройства в аккаунт\n'
#          ' s_pologrudov@mail.ru \n'
#          '      В аккаунт s_pologrudov@mail.ru вошли с нового устройства.\n'
#          '  Если вы этого не делали, измените пароль, чтобы обезопасить '
#          'аккаунт.\n'
#          '  Время 8 февраля, 10:34\n'
#          '  Устройство Mac OS, Google Chrome - неизвестная версия, Москва, '
#          'Россия\n'
#          '  Посмотреть список устройств\n'
#          '  Узнайте, как защитить аккаунт, на нашем сайте по безопасности.\n'
#          '    Вы получили это письмо, потому что являетесь пользователем '
#          'Сервиса Почта Mail\u200c.ru на основании Пользовательского '
#          'соглашения.\n'
#          '  Copyright 2020 Mail\u200c.ru Group, Москва — Все права защищены.\n'
#          '  Служба поддержки\n'
#          '   '}
# {'_id': ObjectId('5e3fbd7848e08b0b480d9a27'),
#  'corr': 'Почта Mail.ru',
#  'date': '31 янв',
#  'link': 'https://e.mail.ru/inbox/1:beef3b95e7fda09e:0/?back=1&afterReload=1',
#  'snippet': 'Почта, Облако, Браузер, Календарь и многое другое. Mail.ru — ваш '
#             'проводник в интернет. Узнайте больш',
#  'sub': 'Mail.ru – больше, чем почта. Познакомьтесь с проектами Mail.ru Group',
#  'text': '  Здравствуйте, Stanislav!\n'
#          '  Mail.ru — ваш проводник в интернет. Узнайте больше о проектах '
#          'Mail.ru Group.\n'
#          '  Подробности\n'
#          'внизу\n'
#          '      Почта\n'
#          '  Пишите и читайте письма, просматривайте и редактируйте файлы и '
#          'фото.\n'
#          '    Облако\n'
#          '  Нужные файлы доступны вам в любой точке мира, с компьютера или '
#          'телефона.\n'
#          '    Браузер Атом\n'
#          '  Попробуйте быстрый, приватный и безопасный браузер от Mail.ru.\n'
#          '    Календарь\n'
#          '  Планируйте задачи и встречи совместно со своими коллегами.\n'
#          '    ICQ\n'
#          '  Общайтесь со своими друзьями и коллегами в режиме реального '
#          'времени.\n'
#          '    ОК\n'
#          '  Ищите старых друзей, вступайте в интересные группы и выкладывайте '
#          'свои фото.\n'
#          '    Мой Мир\n'
#          '  Общайтесь с друзьями, играйте и делитесь фотографиями.\n'
#          '    Новости\n'
#          '  Будьте в курсе главных событий дня.\n'
#          '    Гороскопы\n'
#          '  Узнавайте астрологический прогноз на день для себя и своих '
#          'близких.\n'
#          '    Игры\n'
#          '  Играйте в бесплатные онлайн-игры вместе с друзьями или новыми '
#          'знакомыми.\n'
#          '    Знакомства\n'
#          '  Найдите новых друзей по интересам и, возможно, свою любовь.\n'
#          '    Погода\n'
#          '  Будьте в курсе прогноза погоды, чтобы вовремя захватить зонтик.\n'
#          '    Добро Mail.ru\n'
#          '  Помогайте тем, кто в этом нуждается.\n'
#          '        Следите за нашими новостями в блоге Почты и социальных '
#          'сетях:\n'
#          '                С наилучшими пожеланиями, команда Почты Mail.ru\n'
#          '  Отписаться от рассылки • Служба поддержки\n'
#          '  Mail.ru Group, Москва — Все права защищены.\n'
#          '   '}
# {'_id': ObjectId('5e3fbd7948e08b0b480d9a28'),
#  'corr': 'Почта Mail.ru',
#  'date': '31 янв',
#  'link': 'https://e.mail.ru/inbox/1:a83d9eb4559e59f3:0/?back=1&afterReload=1',
#  'snippet': 'Если это не вы, измените пароль и удалите номер телефона. '
#             'Добавлен номер телефона +1520604 в аккаунт',
#  'sub': 'Добавлен номер телефона +1520604**** в аккаунте',
#  'text': '        Добавлен номер телефона  +1520604****  в аккаунте\n'
#          ' s_pologrudov@mail.ru \n'
#          '      В аккаунте s_pologrudov@mail.ru добавили номер телефона  '
#          '+1520604****.\n'
#          '  Если вы этого не делали:\n'
#          '  1. Измените пароль, чтобы обезопасить аккаунт.\n'
#          '  2. Удалите номер +1520604****, чтобы злоумышленник не смог '
#          'получить доступ к аккаунту снова.\n'
#          '    Вы получили это письмо, потому что являетесь пользователем '
#          'Сервиса Почта Mail\u200c.ru на основании Пользовательского '
#          'соглашения.\n'
#          '  Copyright 2020 Mail\u200c.ru Group, Москва — Все права защищены.\n'
#          '  Служба поддержки\n'
#          '   '}
# {'_id': ObjectId('5e3fbd7a48e08b0b480d9a29'),
#  'corr': 'Почта Mail.ru',
#  'date': '31 янв',
#  'link': 'https://e.mail.ru/inbox/1:e5056c3f00637a3c:0/?back=1&afterReload=1',
#  'snippet': 'Высокоточный поиск, уникальные темы, безлимитное хранилище и '
#             'многое другое. Прочитайте это письмо, ч',
#  'sub': 'Узнайте о супервозможностях Почты Mail.ru',
#  'text': '  Здравствуйте, Stanislav!\n'
#          '  Прочитайте это письмо, чтобы узнать о супервозможностях вашей '
#          'почты\n'
#          '  Подробности\n'
#          'внизу\n'
#          '      Быстрый и простой интерфейс и безлимитное хранилище для писем '
#          'и вложений\n'
#          '      Уникальные темы оформления с прогнозом погоды, результатами '
#          'спортивных состязаний, героями Disney©\n'
#          '        Высокоточный поиск по письмам, вложениям и содержимому '
#          'документов\n'
#          '      Быстрый просмотр и онлайн редактирование фотографий, таблиц, '
#          'документов или презентаций\n'
#          '      Уникальная система правил фильтрации рассылок и мгновенное '
#          'добавление фильтров с помощью перетягивания писем в существующие '
#          'папки\n'
#          '      Лучшее мобильное приложение для iPhone и Android\n'
#          '            Одновременная проверка и параллельное использование '
#          'нескольких почтовых ящиков\n'
#          '  Как добавить почтовый ящик  \n'
#          '    Следите за нашими новостями в блоге Почты и социальных сетях:\n'
#          '                С наилучшими пожеланиями, команда Почты Mail.ru\n'
#          '  Отписаться от рассылки • Служба поддержки\n'
#          '  Mail.ru Group, Москва — Все права защищены.\n'
#          '   '}
# {'_id': ObjectId('5e3fbd7c48e08b0b480d9a2a'),
#  'corr': 'Почта Mail.ru',
#  'date': '31 янв',
#  'link': 'https://e.mail.ru/inbox/1:bed6c2e5bcd7f070:0/?back=1&afterReload=1',
#  'snippet': 'Функции, которые сделают работу с почтой удобнее. Как приложение '
#             'Почты помогает в повседневных делах',
#  'sub': '4 причины установить приложение Почты Mail.ru',
#  'text': '    Здравствуйте, Stanislav!\n'
#          '  Как приложение Почты помогает в повседневных делах\n'
#          '  Установите и попробуйте новые функции:\n'
#          '        Скрыть рассылки, оплатить штрафы и ответить в один клик — в '
#          'Почте можно не только хранить письма. Рассказываем про функции, '
#          'которые помогут вам быстрее решать свои дела.\n'
#          '        УМНАЯ СОРТИРОВКА РАССЫЛОК\n'
#          '  Почта собирает рекламные рассылки в отдельной папке. Так они не '
#          'мешают читать важные письма от коллег или друзей, не путаются с '
#          'регистрационными данными или письмами о заказах.\n'
#          '          УПРАВЛЕНИЕ РАССЫЛКАМИ\n'
#          '  Чтобы отписаться от надоевших рассылок, больше не нужно заходить '
#          'на их сайты и искать, как это сделать. Теперь на одной странице вы '
#          'можете удалить их или отписаться.\n'
#          '            ОПЛАТА ШТРАФОВ\n'
#          '  Почта не оплатит штраф за вождение, но максимально облегчит этот '
#          'процесс. Подключите бесплатные оповещения о новых штрафах и '
#          'оплачивайте их со скидкой 50%.\n'
#          '          УМНЫЕ ОТВЕТЫ\n'
#          '  С помощью технологии Smart Reply вы сможете отвечать на письма '
#          'быстрее. Почта анализирует текст письма и предлагает готовые '
#          'ответы.\n'
#          '      ЕЩЕ В ПОЧТЕ МОЖНО\n'
#          '  Оплачивать мобильный телефон, смотреть видео, фото и документы, '
#          'переводить письма и многое другое.\n'
#          '  Установить приложение\n'
#          '    До встречи в нашем приложении!\n'
#          'Всегда ваша, команда Mail.ru\n'
#          '  Отписаться от рассылки\n'
#          '  Copyright 2020 Mail.ru Group, Москва. Все права защищены.\n'
#          '     '}
#
# Process finished with exit code 0







