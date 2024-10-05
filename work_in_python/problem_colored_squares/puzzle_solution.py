from PIL import Image
import numpy as np
import cv2
import os
import win32gui
import win32con
import win32ui
import time

from working_with_squares import SquareProblem


color_dict = {
    "red": (37, 79, 194),
    "lime": (77, 222, 29),
    "blue": (255, 0, 0),
    "yellow": (16, 235, 220),
    "violet": (222, 22, 240),
    "grey": (105, 118, 122)
}


def get_median_color(image):
    median_color = np.median(image.reshape(-1, 3), axis=0)
    return median_color


def color_to_name(color):
    color = color.astype(int)
    # print(f"Median color: {color}")
    min_distance = float('inf')
    closest_color_name = 'unknown'

    for name, ref_color in color_dict.items():
        distance = np.linalg.norm(color - np.array(ref_color))
        if distance < min_distance:
            min_distance = distance
            closest_color_name = name

    return closest_color_name


def find_game_window(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd != 0:
        return hwnd
    return None


def capture_game_window(window_title):
    hwnd = find_game_window(window_title)
    if hwnd:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)

        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)
        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

        bmp_info = save_bitmap.GetInfo()
        bmp_str = save_bitmap.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGB',
            (bmp_info['bmWidth'], bmp_info['bmHeight']),
            bmp_str, 'raw', 'BGRX', 0, 1
        )
        img.save('screenshot.png', format='PNG')

        save_dc.DeleteDC()
        win32gui.DeleteObject(save_bitmap.GetHandle())
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        print('Снимок экрана сохранен как screenshot.png')
    else:
        print('Окно Pygame не найдено')


capture_game_window('squares game')
image_path = 'screenshot.png'

if not os.path.isfile(image_path):
    print("Файл не найден по пути:", image_path)
else:
    print("Файл найден. Продолжаем обработку.")

    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            image = np.array(img)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        height, width, _ = image.shape
        square_size = width // 6

        result = []

        for row in range(6):
            row_colors = []
            for col in range(6):
                square = image[row * square_size:(row + 1) * square_size, col * square_size:(col + 1) * square_size]
                median_color = get_median_color(square)
                color_name = color_to_name(median_color)
                row_colors.append(color_name)
            result.append(row_colors)

        problem = SquareProblem(result)
        problem.show_squares()
        print("-"*80)
        problem.fill_all_rows()
        problem.show_squares()

    except Exception as e:
        print("Ошибка при обработке изображения:", e)
