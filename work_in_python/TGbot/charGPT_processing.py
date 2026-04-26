import pyautogui
import time
import os
import subprocess
import pyperclip

os.environ["PATH"] += os.pathsep + "/usr/bin" 




pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True
main_text = """У меня есть JSON с сообщениями Telegram (примерно 150 сообщений). 
Сделай промежуточный анализ:
1. Список участников в этом чанке
2. Количество сообщений каждого участника
3. Основные темы обсуждений
4. Стиль общения участников
5. Взаимодействия (кто кому отвечает/цитирует)
Выведи результат в JSON-структуре, чтобы его можно было потом объединить с другими чанками.
можешь всегда ответ давать только json файл без единого слова. Всегда в ответе должен быть только json файл. 
Пришли ответ в формате json а не как обычный текст"""


input("Нажмите Enter чтобы начать выполнение скрипта...")
time.sleep(2)

target_image1 = '/home/georgy-kankiya/projects/test/python/main_test/work_in_python/TGbot/Layer 6 (1).png'
target_image3 = '/home/georgy-kankiya/projects/test/python/main_test/work_in_python/TGbot/Layer 6.png'
target_image2 = '/home/georgy-kankiya/projects/test/python/main_test/work_in_python/TGbot/Layer 6 (1).png'
scroll_amount = 1
scroll_delay = 0.3


for i in range(198, 754):
    while True:
        try:
            location = pyautogui.locateOnScreen(target_image1, confidence=0.6)
            if location:
                print("Нужная часть диалога найдена!")
                center_x, center_y = pyautogui.center(location)
                pyautogui.moveTo(center_x + 100, center_y - 100)
                time.sleep(1)
                break
        except pyautogui.ImageNotFoundException:
            # Если изображение не найдено, скроллим вверх
            print("Изображение не найдено, скроллим вверх...")
            pyautogui.scroll(scroll_amount)
            time.sleep(scroll_delay)
    location = pyautogui.locateOnScreen(target_image2, confidence=0.6)
    center_x, center_y = pyautogui.center(location)
    pyautogui.moveTo(center_x + 100, center_y - 100)
    pyautogui.move(63, 98)
    pyautogui.click()


    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.05)  
    pyautogui.press('backspace')
    time.sleep(0.05)  
    pyperclip.copy(main_text) 
    time.sleep(0.05)  
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    file_path = f"chat_chunks/chat_chunk{i}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        chat_data = f.read()
    pyperclip.copy(chat_data)
    time.sleep(0.05)  
    pyautogui.hotkey("ctrl", "v")

    location = pyautogui.locateOnScreen(target_image3, confidence=0.8)
    center_x, center_y = pyautogui.center(location)
    pyautogui.moveTo(center_x, center_y)
    pyautogui.move(46, 25, duration=0.1)
    pyautogui.click()
    
    region = (1476, 1101, 64, 64)
    image_path = "/home/georgy-kankiya/projects/test/python/main_test/work_in_python/TGbot/Layer 7.png"
    timeout = 50

    start_time = time.time()

    while True:
        try:
            location = pyautogui.locateOnScreen(image_path, region=region, confidence=0.8)
            if location:
                print("Изображение появилось!")
                break
        except pyautogui.ImageNotFoundException:
            # Изображение пока не появилось, продолжаем ждать
            pass

        if time.time() - start_time > timeout:
            print("Время ожидания истекло")
            break

        time.sleep(3)


    for _ in range(5):
        pyautogui.scroll(-200)
        time.sleep(0.05)

    pyautogui.moveTo(768, 959)
    pyautogui.click()
    pyautogui.moveTo(1476, 177)
    pyautogui.click()

    folder = "chunk_ansvers"
    filename = f"chunk_ansver{i}.json"
    path = os.path.join(folder, filename)

    if not os.path.exists(folder):
        os.makedirs(folder)

    text = pyperclip.paste()

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    print("Done:", path)