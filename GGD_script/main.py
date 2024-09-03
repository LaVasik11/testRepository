import pyautogui
import time
import keyboard
import pyautogui
import time

from job_snapshot import get_similar_image


def cleaning_dust_from_paintings():
    x, y = pyautogui.position()
    print(f"Текущие координаты мыши: {x}, {y}")

    pyautogui.moveTo(958, 536, duration=0.1)

    for i in range(20):
        pyautogui.click()
    print("Действия выполнены.")


def check_position():
    x, y = pyautogui.position()
    print(f"Текущие координаты мыши: {x}, {y}")


def fountain_cleaning():
    positions = [(1132, 463), (955, 354), (839, 523), (694, 409)]
    main_position = (1491, 688)

    for i in positions:
        pyautogui.moveTo(*i, duration=0.1)
        pyautogui.mouseDown()
        pyautogui.moveTo(*main_position, duration=0.1)
        pyautogui.mouseUp()


def watch_cleaning():
    positions = [(1037, 271), (1009, 459), (868, 579), (951, 853)]

    for i in positions:
        pyautogui.moveTo(*i, duration=0.1)

        for _ in range(3):
            time.sleep(0.1)
            pyautogui.click()


def stringing():
    positions_from = [(804, 188), (909, 199), (1009, 184), (1114, 201)]
    positions_to = [(747, 1000), (891, 1000), (1027, 1002), (1145, 1010)]

    for i, j in zip(positions_from, positions_to):
        print(i, j)
        pyautogui.moveTo(*i, duration=0.1)
        pyautogui.mouseDown()
        pyautogui.moveTo(*j, duration=0.1)
        pyautogui.mouseUp()


def gramophone_tuning():
    pyautogui.moveTo(948, 896, duration=0.1)
    for _ in range(15):
        pyautogui.click()

    pyautogui.moveTo(1222, 897, duration=0.1)
    for _ in range(9):
        pyautogui.click()
        time.sleep(0.2)


def carpet_cleaning():
    pyautogui.moveTo(1322, 479, duration=0.1)
    pyautogui.mouseDown()
    pyautogui.moveTo(903, 503, duration=0.1)
    pyautogui.moveTo(1189, 188, duration=0.2)

    positions = [(956, 517), (787, 267), (1056, 254), (968, 706), (701, 566)]
    for i in positions:
        pyautogui.moveTo(*i, duration=0.1)
        time.sleep(1.5)

    pyautogui.mouseUp()


keyboard.add_hotkey('ctrl+shift+a', check_position)


actions = {
    "cleaning_dust_from_paintings.png": cleaning_dust_from_paintings,
    "fountain_cleaning.png": fountain_cleaning,
    "watch_cleaning.png": watch_cleaning,
    "stringing.png": stringing,
    "gramophone_tuning.png": gramophone_tuning,
    "carpet_cleaning.png": carpet_cleaning,

}


def execute_action_based_on_image():
    image_name = get_similar_image()
    if image_name in actions:
        actions[image_name]()  # Вызов соответствующей функции
    else:
        print("Нет функции для обработки этого изображения.")


keyboard.add_hotkey('ctrl+shift+1', execute_action_based_on_image)


print("Скрипт запущен. Нажмите Ctrl+Shift+A для выполнения действий.")
keyboard.wait('ctrl+esc')





