
import numpy as np
import keyboard
import pyautogui
import win32api
import win32con
import time
import math

from similar_image import load_images_from_directory, get_similar_image




directory = "task_snapshots"
load_images_from_directory(directory)


def move_wave_fast(start, end, steps=20, amplitude=50, speed=0.001):
    x1, y1 = start
    x2, y2 = end

    for step in range(steps + 1):
        t = step / steps

        x = int(x1 + t * (x2 - x1))
        y = int(y1 + t * (y2 - y1))

        # Добавляем волновую составляющую
        wave_offset = amplitude * math.sin(t * math.pi * 2)
        y += int(wave_offset)

        win32api.SetCursorPos((x, y))
        time.sleep(speed)

def move_wave(start, end, steps=20, amplitude=50, speed=0.02):
    x1, y1 = start
    x2, y2 = end

    for step in range(steps + 1):
        t = step / steps

        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)

        wave_offset = amplitude * math.sin(t * math.pi * 2)

        y += wave_offset
        pyautogui.moveTo(x, y, duration=speed)



def move_arc(A, B, C, steps=50):
    x1, y1 = A
    x2, y2 = B
    cx, cy = C

    # Вычисляем радиус окружности (расстояние от C до A)
    radius = np.sqrt((x1 - cx) ** 2 + (y1 - cy) ** 2)

    angle_A = np.arctan2(y1 - cy, x1 - cx)
    angle_B = np.arctan2(y2 - cy, x2 - cx)

    # Двигаемся против часовой стрелки
    if angle_A > angle_B:
        angle_B += 2 * np.pi

    # Генерация промежуточных точек на полукруге
    for t in np.linspace(angle_A, angle_B, steps):
        x = cx + radius * np.cos(t)
        y = cy + radius * np.sin(t)

        # Перемещение мыши к рассчитанной точке
        pyautogui.moveTo(x, y, duration=0.01)

#####################################################################################################################

def cleaning_dust_from_paintings():
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


def imprint_on_knife():
    pyautogui.moveTo(793, 378, duration=0.1)
    pyautogui.mouseDown()

    for _ in range(10):
        move_wave((890, 644), (544, 882), steps=5, amplitude=10)

    pyautogui.mouseUp()


def imprint_on_rake():
    pyautogui.moveTo(1274, 545, duration=0.1)
    pyautogui.mouseDown()

    for _ in range(10):
        move_wave((1111, 245), (702, 649), steps=5, amplitude=10)

    pyautogui.mouseUp()


def assembling_picture(positions_from, positions_to):
    for i, j in zip(positions_from, positions_to):
        pyautogui.moveTo(*i, duration=0.1)
        pyautogui.mouseDown()
        pyautogui.moveTo(*j, duration=0.1)
        pyautogui.mouseUp()


def assembling_picture1():
    positions_from = [(1421, 572), (1382, 348), (1364, 901), (511, 499), (504, 692)]
    positions_to = [(845, 594), (866, 419), (971, 707), (998, 540), (1031, 416)]

    assembling_picture(positions_from, positions_to)


def assembling_picture2():
    positions_from = [(1388, 693), (1403, 413), (512, 806), (498, 540)]
    positions_to = [(1059, 540), (1004, 683), (879, 480), (870, 636)]

    assembling_picture(positions_from, positions_to)


def assembling_picture3():
    positions_from = [(1232, 694), (552, 840), (1337, 490), (580, 353), (553, 590)]
    positions_to = [(1041, 688), (1037, 454), (846, 612), (873, 449), (882, 782)]

    assembling_picture(positions_from, positions_to)


def cleaning_chess():
    positions = [(1200, 516), (994, 629), (817, 438), (785, 749)]

    for i in positions:
        pyautogui.moveTo(*i, duration=0.1)

        for _ in range(3):
            pyautogui.click()
            time.sleep(0.2)


def fluffing_pillow():
    pyautogui.moveTo(1025, 582, duration=0.1)

    for i in range(30):
        pyautogui.mouseDown()
        pyautogui.mouseUp()


def skull_cleaning():
    positions = [(929, 649), (1130, 335), (512, 862)]

    for _ in range(3):
        for i in positions:
            pyautogui.moveTo(*i, duration=0.1)
            pyautogui.click()


def light_candles():
    positions = [(1186, 474), (984, 486), (785, 478)]

    pyautogui.moveTo(1375, 358, duration=0.1)
    pyautogui.mouseDown()

    for i in positions:
        pyautogui.moveTo(*i, duration=0.1)
        time.sleep(1)

    pyautogui.mouseUp()


def wipe_mirror():
    pyautogui.moveTo(1385, 234, duration=0.1)
    pyautogui.mouseDown()
    
    for _ in range(6):
        pyautogui.moveTo(502, 893, duration=0.2)
        time.sleep(0.1)
        pyautogui.moveTo(1238, 274, duration=0.2)

    pyautogui.mouseUp()


def take_book():
    pyautogui.moveTo(916, 581, duration=0.1)
    pyautogui.mouseDown()
    pyautogui.moveTo(1027, 1073, duration=0.1)
    pyautogui.mouseUp()


def put_book_on_shelf():
    positions = [(440, 325), (1514, 314), (1515, 544), (517, 563), (514, 836), (1508, 843)]

    pyautogui.moveTo(445, 388, duration=0.1)
    pyautogui.mouseDown()

    for n, i in enumerate(positions):
        if n % 2 == 0:
            pyautogui.moveTo(*i, duration=0.1)
        else:
            pyautogui.moveTo(*i, duration=0.6)

    pyautogui.mouseUp()


def fill_bath():
    pyautogui.moveTo(1205, 224, duration=0.1)
    pyautogui.click()


def bush_pruning1():
    pyautogui.moveTo(1039, 786, duration=0.1)
    pyautogui.mouseDown()

    A = (725, 620)
    B = (1560, 517)
    C = (997, 538)

    move_arc(A, B, C, steps=60)

    pyautogui.mouseUp()


def bush_pruning2():
    pyautogui.moveTo(1008, 765, duration=0.1)
    pyautogui.mouseDown()

    A = (531, 652)
    B = (1364, 624)
    C = (988, 760)

    move_arc(A, B, C, steps=65)

    pyautogui.mouseUp()


def eat_dinner():
    pyautogui.moveTo(1081, 731, duration=0.1)

    for _ in range(5):
        pyautogui.click()
        time.sleep(1)


def take_plunger():
    pyautogui.moveTo(1093, 631, duration=0.1)
    pyautogui.click()

    pyautogui.moveTo(1126, 637, duration=0.1)
    pyautogui.mouseDown()
    pyautogui.moveTo(1132, 1058, duration=0.1)
    pyautogui.mouseUp()


def catching_mice():
    positions = [(539, 892), (826, 737), (572, 432), (1139, 377), (1259, 809)]

    time.sleep(2)
    start_time = time.time()
    while time.time() - start_time < 5:
        print(start_time - time.time())
        for i in positions:
            pyautogui.moveTo(*i)
            pyautogui.click()


def hang_up_knives():
    for _ in range(5):
        pyautogui.moveTo(1480, 517, duration=0.1)
        pyautogui.click()
        pyautogui.mouseDown()
        move_wave_fast((1480, 517), (517, 505), 200, 10, 0.005)
        pyautogui.mouseUp()


def toilet_cleaning():
    pyautogui.moveTo(1420, 674, duration=0.1)
    pyautogui.mouseDown()

    for _ in range(12):
        pyautogui.moveTo(1194, 328, duration=0.1)
        pyautogui.moveTo(1173, 355, duration=0.1)

    pyautogui.mouseUp()


def throw_away_trash():
    pyautogui.moveTo(619, 711, duration=0.1)
    pyautogui.mouseDown()
    pyautogui.moveTo(966, 713, duration=0.1)
    pyautogui.mouseUp()


def sweep_leaves():
    positions = [(1120, 779), (1187, 224), (1086, 789), (884, 787), (1047, 201), (915, 841), (745, 810),
                 (936, 145), (761, 829), (574, 780), (831, 141), (699, 191), (593, 633)]

    pyautogui.moveTo(1375, 678, duration=0.1)
    pyautogui.mouseDown()

    for i in positions:
        pyautogui.moveTo(*i)

    pyautogui.mouseUp()


def pour_tea():
    positions = [(1505, 512), (1305, 512), (1050, 508), (801, 523)]

    pyautogui.moveTo(1379, 366, duration=0.1)
    pyautogui.mouseDown()

    for i in positions:
        pyautogui.moveTo(*i, duration=0.1)
        time.sleep(2.2)

    pyautogui.mouseUp()


def cleaning_armor():
    positions = [(958, 124), (950, 985), (493, 909), (1405, 895)]

    pyautogui.moveTo(1375, 229, duration=0.1)
    pyautogui.mouseDown()

    for _ in range(11):
        for i in positions:
            pyautogui.moveTo(*i, duration=0.2)

    pyautogui.mouseUp()


def make_coffee():
    positions = [[(596, 656), (1143, 598), 3.5], [(1139, 839), (1182, 658), 1]]

    for of, to, t in positions:
        pyautogui.moveTo(*of, duration=0.1)
        pyautogui.mouseDown()
        pyautogui.moveTo(*to, duration=0.1)
        pyautogui.mouseUp()
        time.sleep(t)

    pyautogui.moveTo(833, 843, duration=0.1)
    pyautogui.mouseDown()
    pyautogui.moveTo(1269, 675, duration=0.1)
    pyautogui.mouseUp()
    time.sleep(1)
    pyautogui.mouseDown()
    pyautogui.moveTo(833, 843, duration=0.1)
    pyautogui.moveTo(1269, 675, duration=0.1)
    pyautogui.mouseUp()


keyboard.add_hotkey('ctrl+shift+a', check_position)

keyboard.add_hotkey('ctrl+shift+2', make_coffee)


actions = {
    "cleaning_dust_from_paintings.png": cleaning_dust_from_paintings,
    "fountain_cleaning.png": fountain_cleaning,
    "watch_cleaning.png": watch_cleaning,
    "stringing.png": stringing,
    "gramophone_tuning.png": gramophone_tuning,
    "carpet_cleaning.png": carpet_cleaning,
    "cleaning_chess.png": cleaning_chess,
    "fluffing_pillow.png": fluffing_pillow,
    "skull_cleaning.png": skull_cleaning,
    "assembling_picture1.png": assembling_picture1,
    "assembling_picture2.png": assembling_picture2,
    "assembling_picture3.png": assembling_picture3,
    "take_book.png": take_book,
    "put_book_on_shelf1.png": put_book_on_shelf,
    "put_book_on_shelf2.png": put_book_on_shelf,
    "fill_bath.png": fill_bath,
    "light_candles.png": light_candles,
    "wipe_mirror.png": wipe_mirror,
    "eat_dinner.png": eat_dinner,
    "imprint_on_knife.png": imprint_on_knife,
    "bush_pruning1.png": bush_pruning1,
    "bush_pruning2.png": bush_pruning2,
    "take_plunger.png": take_plunger,
    "hang_up_knives.png": hang_up_knives,
    "toilet_cleaning.png": toilet_cleaning,
    "imprint_on_rake.png": imprint_on_rake,
    "throw_away_trash.png": throw_away_trash,
    "sweep_leaves.png": sweep_leaves,
    "pour_tea.png": pour_tea,
    "cleaning_armor.png": cleaning_armor,
    "make_coffee.png": make_coffee,
}


def execute_action_based_on_image():
    image_name = get_similar_image()
    if image_name in actions:
        print(f"Сработала функция: {image_name}")
        actions[image_name]()
    else:
        print("Нет функции для обработки этого изображения.")


keyboard.add_hotkey('ctrl+shift+1', execute_action_based_on_image)


print("Скрипт запущен. Нажмите Ctrl+Shift+A для выполнения действий.")
keyboard.wait('ctrl+esc')





