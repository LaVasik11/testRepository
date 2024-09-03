import os
import cv2
import pyautogui
from PIL import Image
import numpy as np


# Функция для захвата скриншота выбранной области экрана
def take_screenshot(region=None):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot


# Функция для загрузки всех изображений из директории
def load_images_from_directory(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            image_path = os.path.join(directory, filename)
            image = cv2.imread(image_path)
            images.append((filename, image))
    return images


# Функция для сравнения изображений и нахождения наиболее похожего
def find_most_similar_image(screenshot, images):
    best_match = None
    best_match_score = float('inf')

    for filename, image in images:
        # Изменение размера изображения под размер скриншота
        resized_image = cv2.resize(image, (screenshot.shape[1], screenshot.shape[0]))

        # Вычисление разницы между изображениями
        diff = cv2.absdiff(screenshot, resized_image)
        score = np.sum(diff)

        if score < best_match_score:
            best_match_score = score
            best_match = filename

    return best_match


# Основная функция
def get_similar_image():
    region = (100, 100, 300, 200)
    directory = "task_snapshots"

    screenshot = take_screenshot()

    images = load_images_from_directory(directory)

    most_similar_image = find_most_similar_image(screenshot, images)

    if most_similar_image:
        print(f"Наиболее похожее изображение: {most_similar_image}")
        return most_similar_image
    else:
        print("Похожих изображений не найдено.")


if __name__ == '__main__':
    get_similar_image()