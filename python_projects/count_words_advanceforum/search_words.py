import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime
import os


async def fetch_page(session, url, cookies, headers):
    try:
        async with session.get(url, cookies=cookies, headers=headers, timeout=10) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Ошибка: {response.status} для URL: {url}")
                return None
    except asyncio.TimeoutError:
        print(f"TimeoutError для URL: {url}")
        return None
    except Exception as e:
        print(f"Ошибка: {e} для URL: {url}")
        return None


async def process_page(session, url, cookies, headers, word_count):
    page_content = await fetch_page(session, url, cookies, headers)
    if page_content:
        soup = BeautifulSoup(page_content, "html.parser")
        div = soup.find('div', class_='block-body js-replyNewMessageContainer')
        articles = div.find_all('article')[::2] if div else []

        for article in articles:
            div_text = article.find('div', class_='bbWrapper')
            if div_text:
                all_text = div_text.find_all(text=True)
                filtered_text = [
                    text.strip() for text in all_text if text.parent.name != 'blockquote'
                ]
                if filtered_text:
                    word = filtered_text[-1].lower().replace(".", "").strip()
                    word_count[word] += 1


async def process_page_with_progress(session, url, cookies, headers, word_count, progress_tracker):
    await process_page(session, url, cookies, headers, word_count)
    progress_tracker["completed"] += 1
    total = progress_tracker["total"]
    progress = (progress_tracker["completed"] / total) * 100
    print(f"\rПрогресс: {progress:.2f}% ({progress_tracker['completed']}/{total})", end="")


async def main():
    start_time = datetime.now()

    with open("/home/georgy-kankiya/projects/test/python/cookies.json", "r") as f:
        cookies_json = json.load(f)

    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_json}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    output_file = "/home/georgy-kankiya/projects/test/python/word_count.json"
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            word_count = defaultdict(int, json.load(f))
    else:
        word_count = defaultdict(int)

    count_pages = 7352
    max_concurrent_tasks = 10

    processed_pages_file = "/home/georgy-kankiya/projects/test/python/processed_pages.json"
    if os.path.exists(processed_pages_file):
        with open(processed_pages_file, "r", encoding="utf-8") as f:
            processed_pages = set(json.load(f))
    else:
        processed_pages = set()

    remaining_pages = [i for i in range(1, count_pages + 1) if i not in processed_pages]

    progress_tracker = {"completed": 0, "total": len(remaining_pages)}

    semaphore = asyncio.Semaphore(max_concurrent_tasks)

    async with aiohttp.ClientSession() as session:
        try:
            tasks = []
            for i in remaining_pages:
                url = f"https://forum.adv-rp.com/threads/arp-igra-slova.1916258/page-{i}"

                async def sem_task(url=url, page=i):
                    async with semaphore:
                        await process_page_with_progress(session, url, cookies_dict, headers, word_count, progress_tracker)
                        processed_pages.add(page)

                tasks.append(sem_task())

            await asyncio.gather(*tasks)

        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")

        finally:
            sorted_word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))

            with open(output_file, "w", encoding="utf-8") as outfile:
                json.dump(sorted_word_count, outfile, ensure_ascii=False, indent=4, sort_keys=False)

            with open(processed_pages_file, "w", encoding="utf-8") as f:
                json.dump(list(processed_pages), f)

            print(f"\nРезультаты сохранены в {output_file}")
            print(f"Список обработанных страниц сохранён в {processed_pages_file}")

    end_time = datetime.now()
    print("\n\n")
    print("-" * 30)
    print(f"Время выполнения: {end_time - start_time}")


# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())

