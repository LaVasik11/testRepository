import requests
from bs4 import BeautifulSoup
import json
import os


cookies_file = "/home/georgy-kankiya/projects/test/python/cookies.json"

base_url = "https://forum.adv-rp.com/forums/zhaloby-na-administraciju.213/page-{}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def load_cookies(cookies_file):
    if not os.path.exists(cookies_file):
        print(f"Файл {cookies_file} не найден.")
        return {}
    
    with open(cookies_file, "r", encoding="utf-8") as file:
        raw_data = file.read().strip()
        if not raw_data:
            print(f"Файл {cookies_file} пуст.")
            return {}

        try:
            cookies_data = json.loads(raw_data)
        except json.JSONDecodeError as e:
            print(f"Ошибка при разборе JSON: {e}")
            return {}

    cookies = {cookie["name"]: cookie["value"] for cookie in cookies_data}
    return cookies

def process_page(session, page_number):
    url = base_url.format(page_number)
    response = session.get(url)
    
    if response.status_code != 200:
        print(f"Ошибка доступа к странице {page_number}: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.find_all("div", class_="structItem-cell structItem-cell--main")
    
    for div in divs:
        ul = div.find("ul")
        if ul:
            items = ul.find_all("li")
            if len(items) > 1:
                a_tag = div.find("a")
                if a_tag and "href" in a_tag.attrs:
                    link = "https://forum.adv-rp.com/" + a_tag["href"]
                    print(link)

def main():
    cookies = load_cookies(cookies_file)
    if not cookies:
        print("Куки не загружены, завершение работы.")
        return

    with requests.Session() as session:
        session.headers.update(headers)
        session.cookies.update(cookies)

        for page in range(1, 672):
            print(f"Обработка страницы {page}")
            process_page(session, page)

if __name__ == "__main__":
    main()
