import json
import argparse
from telethon.sync import TelegramClient

api_id = 24767972
api_hash = '68606137294b1172deb3e06ad222d645'

parser = argparse.ArgumentParser(description="Telegram message stats tool")
parser.add_argument('--chat', type=str, default="https://t.me/+iA5cLcj47F00NDQ6", help='Ссылка, username или ID группы')
parser.add_argument('--limit', type=int, default=-1, help='Количество сообщений (-1 = все)')
parser.add_argument('--save', type=int, choices=[0, 1], default=0, help='Сохранять сообщения в файл: 1 — да, 0 — нет')
args = parser.parse_args()

client = TelegramClient('session_name', api_id, api_hash)

with client:
    group = client.get_entity(args.chat)
    group_id = group.id
    print(f"ID группы: {group_id}")

    real_limit = None if args.limit == -1 else args.limit
    messages_data = []
    sender_ids = set()

    print(f"Загружаем {'все доступные' if real_limit is None else f'{real_limit}'} сообщений...")

    for i, message in enumerate(client.iter_messages(group_id, limit=real_limit)):
        if message.sender_id and message.text:
            messages_data.append({
                'sender_id': message.sender_id,
                'text': message.text
            })
            sender_ids.add(message.sender_id)

        if real_limit is not None:
            percent = ((i + 1) / args.limit) * 100
            print(f"\rПрогресс: {i + 1}/{args.limit} ({percent:.1f}%)", end='')
        else:
            print(f"\rСобрано сообщений: {i + 1}", end='')

    print(f"\nНайдено сообщений: {len(messages_data)}")
    print(f"Уникальных авторов: {len(sender_ids)}")

    print("Получаем информацию об авторах...")
    id_to_name = {}
    for user_id in sender_ids:
        try:
            user = client.get_entity(user_id)
            id_to_name[user.id] = user.username or user.first_name or "unknown"
        except:
            id_to_name[user_id] = "unknown"

    stats = {}
    final_data = []

    for msg in messages_data:
        user_id = msg['sender_id']
        username = id_to_name.get(user_id, 'unknown')
        text = msg['text']

        if args.save:
            final_data.append({
                'user': username,
                'text': text
            })

        if username not in stats:
            stats[username] = {
                'messages': 0,
                'chars': 0,
                'words': 0
            }

        stats[username]['messages'] += 1
        stats[username]['chars'] += len(text)
        stats[username]['words'] += len(text.split())

    if args.save:
        with open('messages.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        print("\n✅ Сообщения сохранены в messages.json.")

    print("\n📊 Статистика по авторам:")
    for user, s in stats.items():
        print(f"- {user}: сообщений: {s['messages']}, слов: {s['words']}, символов: {s['chars']}\n")









