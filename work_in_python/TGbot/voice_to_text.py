import telebot
import speech_recognition as sr
from pydub import AudioSegment
import os


TOKEN = "6470289113:AAEe6xqDZV_2iP4R8Pap7o0Z18hBd8W5KA0"
bot = telebot.TeleBot(TOKEN)

recognizer = sr.Recognizer()




@bot.message_handler(content_types=['voice'])
def voice_handler(message):
    if message.from_user.id == 7832253194:
        bot.reply_to(
            message,
            "❌ Для тебя конвертация голосовых отключена 🙂"
        )
        return

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    ogg_path = f"voice_{message.message_id}.ogg"
    wav_path = f"voice_{message.message_id}.wav"

    with open(ogg_path, 'wb') as f:
        f.write(downloaded_file)

    audio = AudioSegment.from_ogg(ogg_path)
    audio.export(wav_path, format="wav")

    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        bot.reply_to(message, f"📝 Текст:\n{text}")
    except:
        bot.reply_to(message, "❌ Не удалось распознать речь")

    os.remove(ogg_path)
    os.remove(wav_path)


bot.infinity_polling()
