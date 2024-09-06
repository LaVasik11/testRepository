import pyautogui
import numpy as np


def move_arc(A, B, C, steps=50):
    """
    Перемещает мышь от точки A к точке B через точку C по полукругу.

    :param A: Начальная точка (x, y)
    :param B: Конечная точка (x, y)
    :param C: Вершина полукруга (x, y)
    :param steps: Количество шагов для плавного перемещения
    """
    # Координаты точек A, B и C
    x1, y1 = A
    x2, y2 = B
    cx, cy = C

    # Вычисляем радиус окружности (расстояние от C до A)
    radius = np.sqrt((x1 - cx) ** 2 + (y1 - cy) ** 2)

    # Определяем углы для A и B относительно центра C
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


# Пример использования: перемещение мыши от A к B через C
def bush_pruning1():
    pyautogui.moveTo(1039, 786, duration=0.1)
    pyautogui.mouseDown()

    # Координаты точек
    A = (725, 620)  # Точка A
    B = (1263, 505)  # Точка B
    C = (967, 558)  # Вцершина полукруга C

    move_arc(A, B, C, steps=70)
    pyautogui.mouseUp()


# Запуск функции для проверки
bush_pruning1()
