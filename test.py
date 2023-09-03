from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


data_dict = {'Имя пользователя': 'TestBot№'}

url = 'https://forum.advance-rp.ru/register/'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(1)

input_fields = driver.find_elements(By.CLASS_NAME, 'input')[0:]
labels = driver.find_elements(By.CLASS_NAME, 'formRow-label')[0:]


for i in range(1):
    for label, input_field in zip(labels, input_fields):
        try:
            time.sleep(0.5)
            if label.text == 'Имя пользователя':
                input_field.send_keys(f'TestBot№{i}')
            elif label.text == 'Электронная почта':
                input_field.send_keys(f'BotEmail{i}@yandex.ru')
            elif label.text == 'Пароль':
                input_field.send_keys('password2098715')
            elif label.text == 'Ник в игре':
                input_field.send_keys(f'nik_v_igre{i}')
            elif label.text == 'Сервер':
                input_field.click()
                driver.find_elements(By.TAG_NAME, 'option')[-2].click()
        except:
            pass



time.sleep(100)