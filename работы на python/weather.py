from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def check_the_weather(city):
    '''
    Показывает погоду в заданном городе. Пример использования: check_the_weather('Москва').
    Shows the weather in a given city. Usage example: check_the_weather('Moscow').
    '''
    print('Идёт поиск информации...')
    url = 'https://weather.com/ru-EE/weather/today'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    entry_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'LocationSearch_input')))
    entry_field.send_keys(city)

    first_child_element = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.TAG_NAME, 'button')))
    first_child_element.click()

    weather_data = driver.find_element(By.CLASS_NAME, 'CurrentConditions--primary--2DOqs')
    print('__________________' + '_' * len(city))
    print(f'Погода в городе "{city}":')
    print(weather_data.text)


if __name__ == '__main__':
    check_the_weather(input('Погоду какого города вы хотите узнать?: '))