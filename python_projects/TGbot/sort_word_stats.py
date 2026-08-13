import json

# Загрузка существующего файла
with open("word_stats.json", "r", encoding="utf-8") as f:
    word_stats = json.load(f)

# Сортировка пользователей каждого слова по убыванию количества
for word, data in word_stats.items():
    sorted_users = dict(sorted(data["users"].items(), key=lambda x: x[1], reverse=True))
    word_stats[word]["users"] = sorted_users

# Сортировка слов по общему count по убыванию
sorted_words = dict(sorted(word_stats.items(), key=lambda x: x[1]["count"], reverse=True))

# Сохранение отсортированного файла
with open("word_stats_sorted.json", "w", encoding="utf-8") as f:
    json.dump(sorted_words, f, ensure_ascii=False, indent=4)

print("Сортировка завершена. Результат сохранён в word_stats_sorted.json")
