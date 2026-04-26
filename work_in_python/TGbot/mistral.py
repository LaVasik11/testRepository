import requests
import json
import os
import json
import re
import telebot
import time


TOKEN = "6470289113:AAEe6xqDZV_2iP4R8Pap7o0Z18hBd8W5KA0"
bot = telebot.TeleBot(TOKEN)


# --- Функция обработки сообщений ---
def message_processing(message_text):
    chat = OllamaChat()
    response = chat.send_message(message_text)
    return response


def on_call(message):
    print("Обработка сообщения:", message.text)
    response = message_processing(message.text)
    bot.send_message(message.chat.id, response, reply_to_message_id=message.message_id)


# --- Хендлер для отладки: ловим все сообщения ---
@bot.message_handler(func=lambda m: True)
def debug_all_messages(message):
    print("DEBUG:", message.text)


# --- Фильтр на слово "алиса" ---
@bot.message_handler(func=lambda m: m.text and "алиса" in m.text.lower() and not m.from_user.is_bot)
def handle_message(message):
    print("Фильтр 'алиса' сработал:", message.text)
    on_call(message)


# --- Фильтр на ответы бота ---
@bot.message_handler(func=lambda m: m.reply_to_message and m.reply_to_message.from_user.id == bot.get_me().id and not m.from_user.is_bot)
def handle_reply(message):
    print("Фильтр на ответ бота сработал:", message.text)
    on_call(message)


# --- Хендлер на новых участников (работает только в группах) ---
@bot.chat_member_handler()
def handle_new_member(chat_member):
    if chat_member.new_chat_member.user.id == bot.get_me().id:
        time.sleep(1.5)
        bot.send_message(chat_member.chat.id, "Привет всем!")
        time.sleep(3.5)
        bot.send_message(chat_member.chat.id, "Я алиса, а вас как зовут?")


# --- Класс для общения с Ollama ---
class OllamaChat:
    def __init__(self, model="mistral", system_prompt="Ты играешь роль Александра – мудрого, немного эксцентричного учёного, который увлекается астрономией, коллекционированием редких минералов и игрой на старинном фортепиано. Ты всегда отвечаешь с лёгкой иронией и приводишь интересные примеры."):
        self.model = model
        self.system_prompt = system_prompt
        self.conversation = []

    def build_prompt(self, user_input):
        prompt = f"[SYSTEM] {self.system_prompt}\n"
        for role, message in self.conversation:
            prompt += f"[{role.upper()}] {message}\n"
        prompt += f"[USER] {user_input}\n[ASSISTANT] "
        return prompt

    def send_message(self, user_input):
        prompt = self.build_prompt(user_input)
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {"model": self.model, "prompt": prompt, "stream": False}
        print("Отправка запроса к Ollama...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            assistant_reply = response.json().get("response", "").strip()
            self.conversation.append(("User", user_input))
            self.conversation.append(("Assistant", assistant_reply))
            return assistant_reply
        else:
            return f"Ошибка: {response.status_code}, {response.text}"


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
