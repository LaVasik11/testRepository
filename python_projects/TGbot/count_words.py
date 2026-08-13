from telethon import TelegramClient
from collections import defaultdict
import json
import re

api_id = 24767972
api_hash = "68606137294b1172deb3e06ad222d645"
chat_username = -1002577490080

client = TelegramClient("session_name", api_id, api_hash)
word_stats = defaultdict(lambda: {'count': 0, 'users': defaultdict(int)})

def normalize_word(word):
    word = word.lower()
    word = re.sub(r"[^а-яa-z0-9ё-]", "", word)
    return word

async def main():
    print("Сбор сообщений...")
    total_messages = 0

    async for message in client.iter_messages(chat_username, limit=None):
        total_messages += 1
        if total_messages % 100 == 0:
            print(f"Обработано сообщений: {total_messages}")

        if not message.text or not message.sender:
            continue
        username = message.sender.username or message.sender.first_name or "unknown_user"
        for w in message.text.split():
            word = normalize_word(w)
            if not word:
                continue
            word_stats[word]['count'] += 1
            word_stats[word]['users'][username] += 1

    with open("word_stats.json", "w", encoding="utf-8") as f:
        json.dump(word_stats, f, ensure_ascii=False, indent=4)

    print(f"Готово! Всего обработано сообщений: {total_messages}")
    print("Результат сохранён в word_stats.json")

with client:
    client.loop.run_until_complete(main())