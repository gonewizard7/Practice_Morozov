"""
Выделение цветовых каналов изображения.
"""
import numpy as np
import cv2
from PIL import Image

def extract_channel(cv_img, channel):
    """
    Извлекает указанный цветовой канал в цвете.

    Args:
        cv_img (np.ndarray): изображение BGR
        channel (str): 'r', 'g' или 'b'

    Returns:
        PIL.Image: изображение с выделенным каналом в цвете

    Raises:
        ValueError: при неверном канале
    """
    channel_map = {'b': 0, 'g': 1, 'r': 2}
    if channel not in channel_map:
        raise ValueError("Используйте 'r', 'g' или 'b'")

    # Создаем копию изображения
    extracted = cv_img.copy()

    # Обнуляем другие каналы
    if channel != 'b':
        extracted[:, :, 0] = 0  # Синий канал
    if channel != 'g':
        extracted[:, :, 1] = 0  # Зеленый канал
    if channel != 'r':
        extracted[:, :, 2] = 0  # Красный канал

    # Конвертируем в RGB
    rgb_image = cv2.cvtColor(extracted, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb_image)
