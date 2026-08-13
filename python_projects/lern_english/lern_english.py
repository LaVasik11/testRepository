import tkinter as tk
from googletrans import Translator

import json
import re
import os
import random


base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'words.json')

is_first_click = True

def is_mostly_english(text):
    return re.search('[a-zA-Z]', text) is not None


def is_mostly_russian(text):
    return re.search('[а-яА-Я]', text) is not None


def translate_word(word_to_translate):
    translator = Translator()
    detection = translator.detect(word_to_translate)
    src_lang = detection.lang

    if is_mostly_english(word_to_translate):
        src_lang = 'en'
        dest_lang = 'ru'
    elif is_mostly_russian(word_to_translate):
        src_lang = 'ru'
        dest_lang = 'en'
    else:
        print('Не удалось определить язык', src_lang)
        return "Не удалось определить язык"

    translated_word = translator.translate(word_to_translate, src=src_lang, dest=dest_lang)

    return src_lang, translated_word.text


def handler_translate():
    word = input_field2.get()
    translated_word = translate_word(word)[-1]
    word2.config(text=translated_word)


def add_word():
    word = input_field2.get()
    lang, translated_word = translate_word(word)
    lang_dict = {'en': 'ru',
                 'ru': 'en',
                 }
    word_dict = {lang: word, lang_dict[lang]: translated_word, 'correct answers': 0}

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                data.append(word_dict)
            else:
                data = [word_dict]
    else:
        data = [word_dict]

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    input_field2.delete(0, tk.END)
    word2.config(text="")


def show_word():
    global is_first_click
    list_lang = ['en', 'ru']

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if data:
            random_world = random.choice(data)
            word1.config(text=random_world[random.choice(list_lang)])
            word1.config(bg="white")
            input_field1.delete(0, tk.END)
            is_first_click = True


def examination_word():
    global is_first_click
    verifiable_word = word1.cget('text')
    user_word = input_field1.get()



    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        for n, word_dict in enumerate(data):
            if user_word == '':
                pass

            elif verifiable_word == word_dict.get('ru') and user_word == word_dict.get('en') or \
                    verifiable_word == word_dict.get('en') and user_word == word_dict.get('ru'):
                word1.config(bg="green")

                if (word_dict.get('en') == verifiable_word or word_dict.get('ru') == verifiable_word) and is_first_click:
                    is_first_click = False
                    word_dict['correct answers'] += 1
                    if word_dict['correct answers'] == 5:
                        del data[n]
                    break

                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

            else:
                word1.config(bg="red")

                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for word_dict in data:
                        if word_dict.get('en') == verifiable_word or word_dict.get('ru') == verifiable_word:
                            is_first_click = True

                    word_dict['correct answers'] = 0


        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


root = tk.Tk()
root.title("learn english")
root.geometry("320x165")


root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(3, weight=1)


word1 = tk.Label(text="")
input_field1 = tk.Entry()
button_confirm = tk.Button(text='Проверить', command=examination_word)
button_skip = tk.Button(text='Дальше', command=show_word)

word1.grid(row=1, column=1, columnspan=2, sticky="EW")
word1.config(bg="white")
input_field1.grid(row=2, column=1, columnspan=2, sticky="EW")
button_confirm.grid(row=3, column=2, sticky="EW", padx=5, pady=5)
button_skip.grid(row=3, column=1, sticky="EW", padx=5, pady=5)


separator1 = tk.Frame(height=2, bd=1, relief="sunken")
separator1.grid(row=4, column=1, columnspan=2, sticky="EW", pady=5)


word2 = tk.Label(text="")
input_field2 = tk.Entry()
button_translate = tk.Button(text='Узнать перевод', command=handler_translate)
button_add = tk.Button(text='Добавить слово', command=add_word)

input_field2.grid(row=5, column=1, columnspan=2, sticky="EW")
button_translate.grid(row=6, column=1, sticky="EW", padx=5, pady=5)
button_add.grid(row=6, column=2, sticky="EW", padx=5, pady=5)
word2.grid(row=7, column=1, columnspan=2, sticky="EW")

show_word()
root.mainloop()
