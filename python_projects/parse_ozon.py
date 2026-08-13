from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")


options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win64",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
        )

url = "https://www.ozon.ru/search/?from_global=true&text=поиск+по+продавцу"
driver.get(url)

time.sleep(5)
driver.find_elements(By.CSS_SELECTOR, 'span.a2429-b1.a2429-c5')[-1].click()


elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.le5 div.ea4 div.ae5.ea5 div.ea6")))

print(elements)
for i in elements:
    print(i.text)

driver.quit()
