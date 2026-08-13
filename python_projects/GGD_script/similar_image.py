import os
import cv2
import pyautogui
import numpy as np


images = None


def load_images_from_directory(directory):
    global images
    if images is None:  # Загружаем изображения только один раз
        images = []
        for filename in os.listdir(directory):
            if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
                image_path = os.path.join(directory, filename)
                image = cv2.imread(image_path)
                if image is not None:
                    images.append((filename, image))
                else:
                    print(f"Предупреждение: Не удалось загрузить изображение {filename}.")
    return images


# Функция для захвата скриншота всего экрана
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot


# Функция для поиска наиболее похожего изображения
def find_most_similar_image(screenshot, images):
    best_match = None
    best_match_score = float('inf')

    for filename, image in images:
        resized_image = cv2.resize(image, (screenshot.shape[1], screenshot.shape[0]))
        diff = cv2.absdiff(screenshot, resized_image)
        score = np.sum(diff)

        if score < best_match_score:
            best_match_score = score
            best_match = filename

    return best_match


def get_similar_image():
    global images
    if images is None:
        print("Изображения не загружены.")
        return

    screenshot = take_screenshot()
    most_similar_image = find_most_similar_image(screenshot, images)

    if most_similar_image:
        print(f"Наиболее похожее изображение: {most_similar_image}")
        return most_similar_image
    else:
        print("Похожих изображений не найдено.")