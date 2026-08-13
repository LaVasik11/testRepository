import json
import os
from glob import glob

folder = 'chat_chunks'
chunk_size = 150
file_counter = 0

for filepath in glob(os.path.join(folder, 'chat_chunk*.json')):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.remove(filepath)  # удаляем старый файл

    for i in range(0, len(data), chunk_size):
        part_data = data[i:i+chunk_size]
        if not part_data:
            continue

        new_filename = f"chat_chunk{file_counter}.json"
        new_path = os.path.join(folder, new_filename)
        with open(new_path, 'w', encoding='utf-8') as f:
            json.dump(part_data, f, ensure_ascii=False, indent=2)

        file_counter += 1

