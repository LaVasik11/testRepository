import json, glob
from collections import defaultdict

all_participants = set()
total_message_counts = defaultdict(int)
all_main_topics = set()
all_communication_style = defaultdict(list)
all_interactions = []

for file in glob.glob("chunk_ansvers/chunk_ansver*.json"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Пропускаем некорректный или пустой файл: {file}")
        continue

    if isinstance(data, list):
        data = {"participants": data}

    # Участники
    participants_raw = data.get("participants", [])
    participants = []
    for p in participants_raw:
        if isinstance(p, dict):
            participants.append(p.get("name") or str(p))
        else:
            participants.append(str(p))
    all_participants.update(participants)

    # Сообщения
    message_counts = data.get("message_counts") or data.get("message_count") or {}
    for user, count in message_counts.items():
        total_message_counts[user] += count

    # Основные темы
    topics = data.get("main_topics", [])
    all_main_topics.update(topics)

    # Стиль общения
    comm_style = data.get("communication_style", {})
    for user, style in comm_style.items():
        if isinstance(style, list):
            style = " | ".join(str(s) for s in style)
        elif not isinstance(style, str):
            style = str(style)
        all_communication_style[user].append(style)

    # Взаимодействия
    interactions = data.get("interactions", [])
    for inter in interactions:
        if isinstance(inter, dict):
            normalized_inter = {
                "from": inter.get("from"),
                "to": inter.get("to"),
            }
            if "type" in inter:
                normalized_inter["type"] = inter.get("type")
            if "context" in inter:
                normalized_inter["context"] = inter.get("context")
            if "examples" in inter:
                normalized_inter["examples"] = inter.get("examples")
            if "count" in inter:
                normalized_inter["count"] = inter.get("count")
            all_interactions.append(normalized_inter)
        else:
            all_interactions.append({"raw": str(inter)})

# Объединяем стиль общения
final_communication_style = {}
for user, styles in all_communication_style.items():
    # нормализуем и убираем дубли
    unique_styles = list(dict.fromkeys(filter(None, styles)))
    final_communication_style[user] = " | ".join(unique_styles)

# Финальный JSON
final_data = {
    "participants": sorted(list(all_participants)),
    "message_counts": dict(total_message_counts),
    "main_topics": sorted(list(all_main_topics)),
    "communication_style": final_communication_style,
    "interactions": all_interactions
}

with open("chat_summary.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("Объединение завершено, результат сохранён в chat_summary.json")
