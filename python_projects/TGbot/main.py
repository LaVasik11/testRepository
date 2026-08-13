import os
import json
from telethon import TelegramClient, events, sync
from telethon.tl.types import PeerChannel

api_id = 24767972
api_hash = "68606137294b1172deb3e06ad222d645"
chat_username = -1002577490080
chunk_size = 1500
output_folder = 'chat_chunks'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

client = TelegramClient('session', api_id, api_hash)
client.start()

async def export_chat():
    messages = []
    count = 0
    chunk_index = 1
    user_cache = {}

    async for message in client.iter_messages(chat_username):
        if message.text:
            sender_name = "Unknown"
            if message.sender_id:
                if message.sender_id in user_cache:
                    sender_name = user_cache[message.sender_id]
                else:
                    try:
                        user = await client.get_entity(message.sender_id)
                        sender_name = user.username or f"{user.first_name or ''} {user.last_name or ''}".strip()
                        user_cache[message.sender_id] = sender_name
                    except:
                        sender_name = "Unknown"
                        user_cache[message.sender_id] = sender_name

            messages.append({
                'id': message.id,
                'date': str(message.date),
                'sender_name': sender_name,
                'text': message.text
            })

        count += 1
        if count % 50 == 0:
            print(f'Обработано сообщений: {count}', end='\r')

        if len(messages) >= chunk_size:
            chunk_path = os.path.join(output_folder, f'chat_chunk_{chunk_index}.json')
            with open(chunk_path, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            print(f'\nСохранён файл: {chunk_path}')
            messages = []
            chunk_index += 1

    if messages:
        chunk_path = os.path.join(output_folder, f'chat_chunk_{chunk_index}.json')
        with open(chunk_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        print(f'\nСохранён файл: {chunk_path}')

    print(f'\nЭкспорт завершён. Всего сообщений: {count}')

with client:
    client.loop.run_until_complete(export_chat())